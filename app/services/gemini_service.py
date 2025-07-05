from google import genai
from google.genai import types
from google.genai.types import (
    FunctionDeclaration, Tool,
    GenerateContentConfig, FunctionResponse,
    Content, Part
)

from .function_service import (
    get_branch_wise_deposits,
    get_revenue_sources,
)


def GetPromptResponse(user_input: str, metadata: dict = None) -> str:
    try:
        client = genai.Client(api_key="AIzaSyCcDfOX0UtX67fmLQyaWulSIVAzgL1rShw")

        # 1. Define function declarations
        get_revenue_function = {
            "name": "get_revenue_sources",
            "description": "Get revenue sources from selected branches.",
            "parameters": {
                "type": "object",
                "properties": {
                    "selectedBranches": {"type": "string"},
                    "fromMonth": {"type": "string"},
                    "fromYear": {"type": "string"},
                    "toMonth": {"type": "string"},
                    "toYear": {"type": "string"}
                },
                "required": []
            }
        }

        get_deposit_function = {
            "name": "get_branch_wise_deposits",
            "description": "Get branch-wise deposit data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "selectedBranches": {"type": "string"},
                    "selectedTypes": {"type": "string"},
                    "fromMonth": {"type": "string"},
                    "fromYear": {"type": "string"},
                    "toMonth": {"type": "string"},
                    "toYear": {"type": "string"},
                },
                "required": []
            }
        }


        tools = types.Tool(function_declarations=[
            get_revenue_function,
            get_deposit_function,
            
        ])

        # 2. Add full system instructions
        system_instruction = types.Content(
            role="user",
            parts=[types.Part(text="""    
                You are a smart banking assistant. 
                Always follow these rules:
                1. If the user asks about revenue or deposits, ask them to specify the branch name if it's missing.
                2. If the branch name appears to be misspelled, try fuzzy matching or ask for confirmation.
                3. Interpret 'this quarter' or 'Q1/Q2/etc.' as:
                    - Q1: January – March
                    - Q2: April – June
                    - Q3: July – September
                    - Q4: October – December
                4. If the user mentions 'current month' or 'today', resolve it using the system's current date.
                5. Ignore the day in any DD-MM-YYYY date and only use MM and YYYY.
                6. If both revenue and deposit data are requested, provide both responses clearly.
                7. If optional parameters (like type, month, year) are missing, proceed with the available data.
                8. Respond in INR currency and Lakhs as the unit.
                9. When inputs are ambiguous, ask clarifying questions instead of assuming.  
                10. Intepret all the "month" if mentioned in str as follows:
                        - January-01 or Jan-01 
                        - February-02 or Feb-02
                        - March-03 or Mar-03
                        - April-04 or Apr-04
                        - May-05
                        - June-06 or Jun-06
                        - July-07 or Jul-07
                        - August-08 or Aug-08
                        - September-09 or Sep-09
                        - October-10 or Oct-10
                        - November-11 or Nov-11
                        - December-12 or Dec-12
                11. If optional parameters like type, month, or year are missing:
                        - For year-only input, assume full year (January–December).
                        - If no branch is specified and it's a ranking query (e.g. “highest deposit”), identify the top branch automatically.
                12. If the user asks for highest deposit or top deposit branch, do not ask for a branch name. Call the deposit API without any branch and calculate the branch with highest deposit based on result.
                13. Always use function calling (tools) for any question about revenue or deposits. Never respond from language model alone.
            """)]
        )

        # 3. Prepare conversation content
        contents = [
            system_instruction,
            types.Content(role="user", parts=[types.Part(text=user_input)])
        ]

        # 4. Call Gemini with tool config
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=types.GenerateContentConfig(tools=[tools])
        )

        part = response.candidates[0].content.parts[0]

        if not hasattr(part, "function_call") or not part.function_call:
            return "[Debug] Gemini did not call any function."

        args = part.function_call.args or {}
        if metadata:
            args.update({k: v for k, v in metadata.items() if v is not None})

        # 5. Route function call
        if part.function_call.name == "get_revenue_sources":
            result = ProcessAPIResposne(get_revenue_sources(**args))

        elif part.function_call.name == "get_branch_wise_deposits":
            result = ProcessAPIResposne(get_branch_wise_deposits(**args))

        else:
            result = {"error": "Unknown function"}

        # 6. Follow-up tool return call
        followup_contents = [
            system_instruction,
            contents[1],
            types.Content(role="model", parts=[types.Part(function_call=part.function_call)]),
            types.Content(role="function", parts=[
                types.Part(function_response=FunctionResponse(
                    name=part.function_call.name,
                    response=dict(result=result),
                ))
            ])
        ]

        followup_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=followup_contents
        )

        return followup_response.candidates[0].content.parts[0].text

    except Exception as e:
        return f"Unhandled error: {str(e)}"


def ProcessAPIResposne(result_raw):
    result = []
    for item in result_raw:
        category = item.get('category') or item.get("branch") or item.get("type") or "N/A"
        value = item.get('value') or item.get("amount") or "0"
        transformed_item = {
            "revenue_source_type": category,
            "revenue_generated": value,
            "Currency": "INR",
            "Unit": "Lakhs"
        }
        result.append(transformed_item)
    return result

