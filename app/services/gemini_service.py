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


def parallel_api_call(args):
    app = current_app._get_current_object()
    key_bytes = app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
    iv_bytes = app.config['AES_IV_STRING'].encode('utf-8')

    def call_revenue():
        return get_revenue_sources(**args, key_bytes=key_bytes, iv_bytes=iv_bytes)

    def call_deposit():
        return get_branch_wise_deposits(**args, key_bytes=key_bytes, iv_bytes=iv_bytes)

    with ThreadPoolExecutor() as executor:
        revenue_future = executor.submit(call_revenue)
        deposit_future = executor.submit(call_deposit)
        return revenue_future.result(), deposit_future.result()


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
            "revenue_source_type": category,
            "revenue_generated": value,
            "Currency": "INR",
            "Unit": "Lakhs",
        }
        result.append(transformed_item)

    print("\n[API] Transformed result for Gemini:", result)
    return result
