import re
import json
import codecs
from concurrent.futures import ThreadPoolExecutor
from flask import current_app
from google import genai
from google.genai import types
from google.genai.types import (
    FunctionDeclaration, Tool,
    GenerateContentConfig, FunctionResponse,
    Content, Part
)

from app.services.function_service import get_branch_wise_deposits, get_revenue_sources

def decode_unicode_escapes(text):
    if isinstance(text, str):
        return codecs.decode(text, 'unicode_escape')
    return text

def GetPromptResponse(user_input: str, metadata: dict = None) -> str:
    try:
        client = genai.Client(api_key="AIzaSyCPACKAszEIfA5gO3eRWDlzQ57q3zmYo_w")  # Replace with secure loading

        args = metadata or {}

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
                }
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
                    "toYear": {"type": "string"}
                }
            }
        }

        tools = types.Tool(function_declarations=[get_revenue_function, get_deposit_function])

        system_instruction = types.Content(
            role="user",
            parts=[types.Part(text="""
                You are a smart banking assistant.
                Always follow these rules:
                1. If the user asks for any details without mentioning branch name, assume it's for "all" branches.
                2. Interpret 'this quarter' or 'Q1/Q2/etc.' as:
                   - Q1: January – March
                   - Q2: April – June
                   - Q3: July – September
                   - Q4: October – December
                3. If the user mentions 'current month' or 'today', resolve it using the system's current date.
                4. Ignore the day in any DD-MM-YYYY date and only use MM and YYYY.
                5. If optional parameters (like type, month, year) are missing, proceed with the available data.
                6. Interpret all "month" mentions in strings as:
                   - January: 01 or Jan
                   - February: 02 or Feb
                   - March: 03 or Mar
                   - April: 04 or Apr
                   - May: 05
                   - June: 06 or Jun
                   - July: 07 or Jul
                   - August: 08 or Aug
                   - September: 09 or Sep
                   - October: 10 or Oct
                   - November: 11 or Nov
                   - December: 12 or Dec
                7. For year-only inputs, assume full year (January–December).
                8. If no branch is specified and it's a ranking query (e.g. “highest deposit”), identify the top branch automatically.
                9. If the user asks for highest deposit or top deposit branch, do not ask for a branch name. Call the deposit API without any branch and calculate the branch with highest deposit.
                10. If the user does not provide a time period (month/year), do not ask for it.
                    Assume a default period of the most recent complete quarter or entire current year depending on the context.
                11. If both revenue and deposit data are asked in the same query, trigger both functions in parallel and combine the response.
                12. If user input mentions multiple branches (e.g., "for Udupi branch and Manipal branch"), extract all branches mentioned and treat them as a comma-separated list in selectedBranches.
            """)]
        )

        contents = [
            system_instruction,
            types.Content(role="user", parts=[types.Part(text=user_input)])
        ]

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=types.GenerateContentConfig(tools=[tools])
        )

        parts = response.candidates[0].content.parts
        print("\n[Gemini] Full parts from model:", parts)

        followup_parts = []
        function_calls = []

        for part in parts:
            if hasattr(part, 'function_call') and part.function_call:
                function_calls.append(part.function_call)

        if len(function_calls) >= 1:
            for function_call in function_calls:
                print(f"\n[Gemini] Requested function: {function_call.name}")
                print(f"[Gemini] With arguments: {function_call.args}")

                args = function_call.args or {}
                if metadata:
                    args.update({k: v for k, v in metadata.items() if v is not None})

                app = current_app._get_current_object()
                key_bytes = app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
                iv_bytes = app.config['AES_IV_STRING'].encode('utf-8')

                try:
                    if function_call.name == "get_revenue_sources":
                        api_result = ProcessAPIResposne(get_revenue_sources(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_branch_wise_deposits":
                        api_result = ProcessAPIResposne(get_branch_wise_deposits(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    else:
                        api_result = {"error": "Function not found."}
                except Exception as e:
                    api_result = {"error": str(e)}

                followup_parts.extend([
                    types.Content(role="model", parts=[types.Part(function_call=function_call)]),
                    types.Content(role="function", parts=[types.Part(
                        function_response=FunctionResponse(
                            name=function_call.name,
                            response=dict(result=api_result),
                        )
                    )])
                ])

            followup_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[system_instruction, contents[1]] + followup_parts
            )

            return followup_response.candidates[0].content.parts[0].text

        else:
            # ✅ No function call, just return the Gemini text naturally
            for part in parts:
                if hasattr(part, "text") and part.text.strip():
                    return part.text.strip()

            return "Sorry, I couldn't generate a response."  # Should not hit this unless all parts empty

    except Exception as e:
        return f"Unhandled error: {str(e)}"

def GetPromptResponseNew(user_input: str, metadata: dict = None) -> str:
    """
    Handles user prompts, interacts with the Gemini model, and orchestrates
    function calls (both parallel and compositional).
    """
    try:
        # IMPORTANT: Replace "YOUR_API_KEY" with a secure method of loading your API key.
        # Do not hardcode API keys in production environments.
        client = genai.Client(api_key="AIzaSyCPACKAszEIfA5gO3eRWDlzQ57q3zmYo_w")

        # Define function declarations for Gemini
        get_revenue_declaration = types.FunctionDeclaration(
            name="get_revenue_sources",
            description="Get revenue sources from selected branches.",
            parameters={
                "type": "object",
                "properties": {
                    "selectedBranches": {"type": "string", "description": "Comma-separated list of branch names (e.g., 'Udupi, Manipal') or 'all' for all branches."},
                    "fromMonth": {"type": "string", "description": "Starting month (e.g., '01' for January, 'Jan')."},
                    "fromYear": {"type": "string", "description": "Starting year (e.g., '2023')."},
                    "toMonth": {"type": "string", "description": "Ending month (e.g., '12' for December, 'Dec')."},
                    "toYear": {"type": "string", "description": "Ending year (e.g., '2024')."}
                },
                "required": ["selectedBranches"]
            }
        )

        get_deposit_declaration = types.FunctionDeclaration(
            name="get_branch_wise_deposits",
            description="Get branch-wise deposit data.",
            parameters={
                "type": "object",
                "properties": {
                    "selectedBranches": {"type": "string", "description": "Comma-separated list of branch names (e.g., 'Udupi, Manipal') or 'all' for all branches."},
                    "selectedTypes": {"type": "string", "description": "Comma-separated list of deposit types (e.g., 'Savings, Fixed Deposit')."},
                    "fromMonth": {"type": "string", "description": "Starting month (e.g., '01' for January, 'Jan')."},
                    "fromYear": {"type": "string", "description": "Starting year (e.g., '2023')."},
                    "toMonth": {"type": "string", "description": "Ending month (e.g., '12' for December, 'Dec')."},
                    "toYear": {"type": "string", "description": "Ending year (e.g., '2024')."}
                },
                "required": ["selectedBranches"]
            }
        )

        # Combine all function declarations into a list of Tool objects
        tools_list = [
            types.Tool(function_declarations=[get_revenue_declaration]),
            types.Tool(function_declarations=[get_deposit_declaration])
        ]

        # System instructions as a persistent part of the conversation context
        system_instruction_text = """
            You are a smart banking assistant.
            Always follow these rules:
            1. If the user asks for any details without mentioning branch name, assume it's for "all" branches.
            2. Interpret 'this quarter' or 'Q1/Q2/etc.' as:
               - Q1: January – March
               - Q2: April – June
               - Q3: July – September
               - Q4: October – December
            3. If the user mentions 'current month' or 'today', resolve it using the system's current date.
            4. Ignore the day in any DD-MM-YYYY date and only use MM and YYYY.
            5. If optional parameters (like type, month, year) are missing, proceed with the available data.
            6. Interpret all "month" mentions in strings as:
               - January: 01 or Jan
               - February: 02 or Feb
               - March: 03 or Mar
               - April: 04 or Apr
               - May: 05
               - June: 06 or Jun
               - July: 07 or Jul
               - August: 08 or Aug
               - September: 09 or Sep
               - October: 10 or Oct
               - November: 11 or Nov
               - December: 12 or Dec
            7. For year-only inputs, assume full year (January–December).
            8. If no branch is specified and it's a ranking query (e.g. “highest deposit”), identify the top branch automatically.
            9. If the user asks for highest deposit or top deposit branch, do not ask for a branch name. Call the deposit API without any branch and calculate the branch with highest deposit.
            10. If the user does not provide a time period (month/year), do not ask for it.
                Assume a default period of the most recent complete quarter or entire current year depending on the context.
            11. If both revenue and deposit data are asked in the same query, trigger both functions in parallel and combine the response.
            12. If user input mentions multiple branches (e.g., "for Udupi branch and Manipal branch"), extract all branches mentioned and treat them as a comma-separated list in selectedBranches.
        """
        system_instruction_part = types.Part(text=system_instruction_text)

        # Initialize conversation history with the user's initial prompt
        conversation_history = [
            types.Content(role="user", parts=[types.Part(text=user_input)])
        ]

        MAX_TURNS = 5 # Safety break to prevent infinite loops during compositional calls
        turn_count = 0

        while turn_count < MAX_TURNS:
            turn_count += 1
            print(f"\n--- Turn {turn_count} of interaction with Gemini ---")

            # Call generate_content with the full conversation history.
            # The system instruction is prepended to ensure it's always considered first.
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[types.Content(role="user", parts=[system_instruction_part])] + conversation_history,
                config=types.GenerateContentConfig(tools=tools_list)
            )

            parts = response.candidates[0].content.parts
            print(f"\n[Gemini] Full parts from model (Turn {turn_count}):", parts)

            function_calls_this_turn = []
            final_text_response = ""

            # Separate function calls from potential text responses in this turn
            for part in parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_calls_this_turn.append(part.function_call)
                elif hasattr(part, 'text') and part.text.strip():
                    final_text_response = part.text.strip()

            if not function_calls_this_turn:
                # If no function calls are suggested, and there's a text response,
                # it means Gemini is done and provides the final answer.
                if final_text_response:
                    print(f"\n[Gemini] Final text response (Turn {turn_count}):", final_text_response)
                    return final_text_response
                else:
                    # No function calls and no text, might be an issue or end of conversation
                    print(f"\n[Gemini] No function calls or final text response in turn {turn_count}. Ending interaction.")
                    return "Sorry, I couldn't generate a complete response. Please try again."

            # Add Gemini's function call suggestions to the conversation history
            # This is crucial for the model to remember what it asked for.
            for fc in function_calls_this_turn:
                conversation_history.append(types.Content(role="model", parts=[types.Part(function_call=fc)]))

            # Execute all suggested function calls (potentially in parallel for this turn)
            function_responses_to_add = []
            for function_call in function_calls_this_turn:
                print(f"\n[Gemini] Requested function: {function_call.name}")
                print(f"[Gemini] With arguments: {function_call.args}")

                # Ensure arguments are treated as a dictionary
                args = function_call.args or {}
                if metadata:
                    # Merge metadata, allowing metadata values to override if keys conflict
                    args.update({k: v for k, v in metadata.items() if v is not None})

                # Retrieve AES encryption keys from Flask's current_app config
                # Ensure your Flask app is set up to provide these keys.
                try:
                    app = current_app._get_current_object()
                    key_bytes = app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
                    iv_bytes = app.config['AES_IV_STRING'].encode('utf-8')
                except RuntimeError:
                    # Handle case where current_app is not available (e.g., during testing outside Flask context)
                    print("[WARNING] Flask current_app not available. Using dummy encryption keys.")
                    key_bytes = b'0123456789abcdef0123456789abcdef' # Dummy key
                    iv_bytes = b'0123456789abcdef' # Dummy IV

                api_result = {"error": "Function execution failed due to unhandled error."} # Default error

                try:
                    if function_call.name == "get_revenue_sources":
                        api_result = ProcessAPIResposne(get_revenue_sources(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_branch_wise_deposits":
                        api_result = ProcessAPIResposne(get_branch_wise_deposits(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    else:
                        api_result = {"error": f"Function '{function_call.name}' not found or implemented."}
                except Exception as e:
                    api_result = {"error": f"Error during API call for {function_call.name}: {str(e)}"}
                    print(f"[ERROR] Function execution failed for {function_call.name}: {e}")

                # Add the function response to the list for this turn
                function_responses_to_add.append(
                    types.Content(
                        role="function",
                        parts=[types.Part(
                            function_response=FunctionResponse(
                                name=function_call.name,
                                response=dict(result=api_result), # Wrap result in a dict with 'result' key
                            )
                        )]
                    )
                )

            # Add all function responses from this turn to the conversation history
            conversation_history.extend(function_responses_to_add)

            # The loop will continue, and in the next iteration, Gemini will be prompted
            # with the updated conversation_history (including the function results),
            # allowing it to decide if another function call or a final text response is needed.

        # If the loop completes without returning, it means MAX_TURNS was exceeded.
        print(f"\n[WARNING] Exceeded MAX_TURNS ({MAX_TURNS}). Returning a generic error or last known text.")
        # Attempt to return the last text part if available, otherwise a generic message.
        if final_text_response:
             return final_text_response
        return "Sorry, I could not complete your request after several attempts. Please try again or rephrase."

    except Exception as e:
        print(f"[CRITICAL ERROR] Unhandled error in GetPromptResponse: {str(e)}")
        return f"An internal error occurred: {str(e)}"



def ProcessAPIResposne(result_raw):
    print("\n[API] Raw result received:", result_raw)

    if isinstance(result_raw, str):
        try:
            result_raw = json.loads(result_raw)
        except Exception:
            return [{"error": "Invalid string response from API", "raw": result_raw}]

    if isinstance(result_raw, dict) and "error" in result_raw:
        return [{"error": result_raw["error"]}]

    if not isinstance(result_raw, list):
        return [{"error": "Unexpected API response format", "raw": result_raw}]

    result = []
    for item in result_raw:
        if not isinstance(item, dict):
            continue
        category = decode_unicode_escapes(item.get('category') or item.get("branch") or item.get("type") or "N/A")
        value = decode_unicode_escapes(str(item.get('value') or item.get("amount") or "0"))

        transformed_item = {
            "Category": category,
            "Value": value,
            "Currency": "INR",
            "Unit": "Lakhs",
        }
        result.append(transformed_item)

    print("\n[API] Transformed result for Gemini:", result)
    return result
