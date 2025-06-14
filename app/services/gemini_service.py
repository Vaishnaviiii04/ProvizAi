from google import genai
from google.genai import types
from google.genai.types import (
    FunctionDeclaration, Tool,
    GenerateContentConfig, FunctionResponse,
    Content, Part
)

from app.services.function_service import get_branch_wise_deposits, get_revenue_sources

def GetPromptResponse(user_input: str, metadata: dict = None) -> str:
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
            "required": ["selectedBranches"]
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
                "UserId": {"type": "string"},
                "Last_SignedIn_Time": {"type": "string"},
                "Bank_Id": {"type": "string"},
                "AppVersion": {"type": "string"},
                "Platform": {"type": "string"}
            },
            "required": ["selectedBranches"]
        }
    }

    tools = types.Tool(function_declarations=[get_revenue_function, get_deposit_function])
    system_instruction = types.Content(
        role="user",
        parts=[types.Part(text="You're a smart banking assistant. Provide clear summaries of revenue and deposits.")]
    )

    client = genai.Client(api_key="AIzaSyCcDfOX0UtX67fmLQyaWulSIVAzgL1rShw")
    contents = [
        system_instruction,
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=types.GenerateContentConfig(tools=[tools])
    )

    part = response.candidates[0].content.parts[0]
    if part.function_call:
        args = part.function_call.args or {}
        if metadata:
            args.update({k: v for k, v in metadata.items() if v is not None})

        if part.function_call.name == "get_revenue_sources":
            result = get_revenue_sources(**args)
        elif part.function_call.name == "get_branch_wise_deposits":
            result = get_branch_wise_deposits(**args)
        else:
            result = {"error": "Function not found."}

        followup_contents = [
            system_instruction,
            contents[1],
            types.Content(role="model", parts=[types.Part(function_call=part.function_call)]),
            types.Content(
                role="function",
                parts=[
                    types.Part(function_response=FunctionResponse(
                        name=part.function_call.name,
                        response=result
                    )),
                    types.Part(text="Function executed.")
                ]
            )
        ]
        followup_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=followup_contents
        )
        return followup_response.candidates[0].content.parts[0].text
    else:
        return part.text
