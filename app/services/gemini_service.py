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

from app.services.function_service import (
    get_branch_wise_deposits, get_revenue_sources,
    get_income_expenditure,get_monthly_profit,get_areawise_deposits,
    get_castewise_deposits,get_member_vs_nonmember_deposits,
    get_deposit_categories,get_deposit_interest_rate,get_monthly_deposit_volume,
    get_monthly_deposit_count,get_monthly_closed_deposit_count,
    get_monthly_closed_deposit_volume,get_monthly_renewed_deposit_count,
    get_monthly_renewed_deposit_volume,get_branch_wise_loans,
    get_loan_categories,get_type_wise_npa_loans,get_status_wise_npa_loans,
    get_type_wise_no_of_loans,get_monthly_loans_volume,get_loan_interest_rate_distribution,
    get_monthly_loan_recovery_count,get_monthly_loan_recovery_volume,
    get_type_wise_transactions_volume,get_type_wise_transactions_count,
    get_branch_wise_transactions_volume,get_branch_wise_transactions_count,
    get_branch_wise_app_users,get_monthly_transactions_count,get_monthly_transactions_volume,
    get_monthly_pigmy_collection_volume,get_online_payments_volume,get_online_payments_count,
    get_online_collections_volume,get_online_collections_count,get_branch_wise_customers,
    get_caste_wise_customers,get_gender_wise_customers,get_area_wise_customers,
    get_village_wise_customers,get_age_distribution)

def decode_unicode_escapes(text):
    if isinstance(text, str):
        return codecs.decode(text, 'unicode_escape')
    return text

def GetPromptResponse(user_input: str, metadata: dict = None) -> str:
    try:
        client = genai.Client(api_key="YOUR_API_KEY")  # Replace with secure loading

        args = metadata or {}
        

        get_revenue_function = {
            "name": "get_revenue_sources",
            "description": "Get revenue sources .",
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

        get_income_expenditure_function = {
            "name": "get_income_expenditure",
            "description": "Get income and expenditure data .",
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

        get_monthly_profit_function = {
            "name": "get_monthly_profit",
            "description": "Get monthly profit details .",
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

        get_areawise_deposit_function = {
            "name": "get_areawise_deposits",
            "description": "Get area-wise deposit data .",
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

        get_castewise_deposit_function = {
            "name": "get_castewise_deposits",
            "description": "Get caste-wise deposit data .",
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

        get_member_vs_nonmember_deposit_function = {
            "name": "get_member_vs_nonmember_deposits",
            "description": "Get member vs non-member deposit data.",
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

        get_deposit_categories_function = {
            "name": "get_deposit_categories",
            "description": "Get deposit category-wise data.",
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

        get_deposit_interest_rate_function = {
            "name": "get_deposit_interest_rate",
            "description": "Get deposit interest rate data .",
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

        get_monthly_deposit_volume_function = {
            "name": "get_monthly_deposit_volume",
            "description": "Get monthly deposit volume data .",
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

        get_monthly_deposit_count_function = {
            "name": "get_monthly_deposit_count",
            "description": "Get monthly deposit count data.",
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

        get_monthly_closed_deposit_count_function = {
            "name": "get_monthly_closed_deposit_count",
            "description": "Get monthly closed deposit count data .",
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

        get_monthly_closed_deposit_volume_function = {
            "name": "get_monthly_closed_deposit_volume",
            "description": "Get monthly closed deposit volume data.",
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

        get_monthly_renewed_deposit_count_function = {
            "name": "get_monthly_renewed_deposit_count",
            "description": "Get monthly renewed deposit count data.",
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

        get_monthly_renewed_deposit_volume_function = {
            "name": "get_monthly_renewed_deposit_volume",
            "description": "Get monthly renewed deposit volume data.",
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

        get_branch_wise_loans_function = {
            "name": "get_branch_wise_loans",
            "description": "Get branch-wise loan data.",
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

        get_loan_categories_function = {
            "name": "get_loan_categories",
            "description": "Get  loan category-wise data .",
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

        get_type_wise_npa_loans_function = {
            "name": "get_type_wise_npa_loans",
            "description": "Get type-wise NPA loan data .",
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

        get_status_wise_npa_loans_function = {
            "name": "get_status_wise_npa_loans",
            "description": "Get status-wise NPA loan data.",
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

        get_type_wise_no_of_loans_function = {
            "name": "get_type_wise_no_of_loans",
            "description": "Get type-wise number of loan data.",
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

        get_monthly_loans_volume_function = {
            "name": "get_monthly_loans_volume",
            "description": "Get monthly loans volume data.",
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

        get_loan_interest_rate_distribution_function = {
            "name": "get_loan_interest_rate_distribution",
            "description": "Get loan interest rate distribution data.",
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

        get_monthly_loan_recovery_count_function = {
            "name": "get_monthly_loan_recovery_count",
            "description": "Get monthly loan recovery count data.",
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

        get_monthly_loan_recovery_volume_function = {
            "name": "get_monthly_loan_recovery_volume",
            "description": "Get monthly loan recovery volume data .",
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

        get_type_wise_transactions_volume_function = {
            "name": "get_type_wise_transactions_volume",
            "description": "Get type-wise transaction volume data .",
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

        get_type_wise_transactions_count_function = {
            "name": "get_type_wise_transactions_count",
            "description": "Get type-wise transaction count data .",
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

        get_branch_wise_transactions_volume_function = {
            "name": "get_branch_wise_transactions_volume",
            "description": "Get branch-wise transactions volume data .",
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

        get_branch_wise_transactions_count_function = {
            "name": "get_branch_wise_transactions_count",
            "description": "Get branch-wise transactions count data for selected branches.",
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
       
        get_branch_wise_app_users_function = {
            "name": "get_branch_wise_app_users",
            "description": "Get branch-wise app user data.",
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

        get_monthly_transactions_count_function = {
            "name": "get_monthly_transactions_count",
            "description": "Get monthly transactions count data.",
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
       
        get_monthly_transactions_volume_function= {
            "name": "get_monthly_transactions_volume",
            "description": "Get monthly transactions volume data.",
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
        get_monthly_pigmy_collection_volume_function= {
            "name": "get_monthly_pigmy_collection_volume",
            "description": "Get monthly pigmy collection volume data .",
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

        get_online_payments_volume_function= {
            "name": "get_online_payments_volume",
            "description": "Get monthly online payments volume data .",
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

        get_online_payments_count_function= {
            "name": "get_online_payments_count",
            "description": "Get monthly online payments count data .",
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

        get_online_collections_volume_function= {
            "name": "get_online_collections_volume",
            "description": "Get monthly online collections volume data .",
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

        get_online_collections_count_function= {
            "name": "get_online_collections_count",
            "description": "Get monthly online collections count data .",
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

        get_branch_wise_customers_function= {
            "name": "get_branch_wise_customers",
            "description": "Get branch wise customers data.",
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
       
        get_caste_wise_customers_function= {
            "name": "get_caste_wise_customers",
            "description": "Get caste wise customers data. ",
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
       
        get_gender_wise_customers_function= {
            "name": "get_gender_wise_customers",
            "description": "Get gender wise customers data .",
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
       
        get_area_wise_customers_function= {
            "name": "get_area_wise_customers",
            "description": "Get area wise customers data.",
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

        get_village_wise_customers_function= {
            "name": "get_village_wise_customers",
            "description": "Get village wise customers data.",
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
       
        get_age_distribution_function= {
            "name": "get_age_distribution",
            "description": "get age distribution data.",
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


        tools = types.Tool(function_declarations=[get_revenue_function,get_income_expenditure_function,
        get_monthly_profit_function, get_deposit_function,get_areawise_deposit_function,
        get_castewise_deposit_function,get_member_vs_nonmember_deposit_function,
        get_deposit_categories_function,get_deposit_interest_rate_function,get_monthly_deposit_volume_function,
        get_monthly_deposit_count_function,get_monthly_closed_deposit_count_function,
        get_monthly_closed_deposit_volume_function,get_monthly_renewed_deposit_count_function,
        get_monthly_renewed_deposit_volume_function,get_branch_wise_loans_function,
        get_loan_categories_function,get_type_wise_npa_loans_function,get_status_wise_npa_loans_function,
        get_type_wise_no_of_loans_function,get_monthly_loans_volume_function,
        get_loan_interest_rate_distribution_function,get_monthly_loan_recovery_count_function,
        get_monthly_loan_recovery_volume_function,get_type_wise_transactions_volume_function,
        get_type_wise_transactions_count_function,get_branch_wise_transactions_volume_function,
        get_branch_wise_transactions_volume_function,get_branch_wise_app_users_function,
        get_monthly_transactions_count_function,get_monthly_transactions_volume_function,
        get_monthly_pigmy_collection_volume_function,get_online_payments_volume_function,
        get_online_payments_count_function,get_online_collections_volume_function,
        get_online_collections_count_function,get_branch_wise_customers_function,
        get_caste_wise_customers_function,get_gender_wise_customers_function,get_area_wise_customers_function,
        get_village_wise_customers_function,get_age_distribution_function
        ])

        system_instruction = types.Content(
            role="user",
            parts=[types.Part(text="""
You are a smart banking assistant. Follow these rules strictly for every user prompt:

1. Branch Handling:
   - If the user does not mention a branch, assume "all branches".
   - If multiple branches are mentioned (e.g., “Udupi and Manipal”), extract all and pass as a comma-separated list.
   - For ranking queries (e.g., "highest deposit", "top branch for loans"):
     - Do NOT ask the user for a branch name.
     - Automatically analyze across all branches and identify the top one using available data.

2. Time Period Handling:
   - If the user does not specify a time period (month, year, or date), DO NOT ask for it.
   - Always assume the following default:
     - Use the **entire current calendar year** (January to December).
     - Only use a specific quarter if the user **explicitly mentions it** (e.g., “Q1”, “this quarter”, etc.).
   - For "current month" or "today", resolve based on the system’s current date.
   - If the user gives a full date (DD-MM-YYYY), ignore the day and use only the month and year.
   - Never prompt the user to provide missing time inputs unless critically required for the query.

3. Deposit Type Handling:
   - If the user does not mention deposit types, assume **all types** by default.
   - Do NOT ask the user which deposit types they are interested in.

4. Optional Parameters:
   - If the user does not provide optional parameters (like deposit types, year, or branch), use a smart default and continue.
   - Do NOT delay execution or ask the user to fill in missing optional data.

5. Month Conversion:
   Convert all month names or short forms to two-digit numeric strings:
   - Jan → 01, Feb → 02, Mar → 03, Apr → 04, May → 05, Jun → 06
   - Jul → 07, Aug → 08, Sep → 09, Oct → 10, Nov → 11, Dec → 12

6. Parallel Function Calls:
   - If a prompt involves multiple categories (e.g., deposits + revenue), trigger all related APIs in parallel and combine their results cleanly.

7. Response Behavior:
   - Be direct and professional. Never restate the user’s question.
   - Avoid follow-up questions unless the input is truly ambiguous and cannot be resolved.
   - Output structured, clear insights (e.g., tables, rankings, summaries) wherever helpful.

These rules apply to all banking-related queries: deposits, loans, transactions, customer data, analytics, and more.
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
        if response.usage_metadata:
                print(f"Prompt tokens (input): {response.usage_metadata.prompt_token_count}")
                print(f"Candidates tokens (output): {response.usage_metadata.candidates_token_count}")
                print(f"Total tokens (input + output): {response.usage_metadata.total_token_count}")
        else:
                print("No usage_metadata found in the response.")       
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
                    elif function_call.name == "get_income_expenditure":
                        api_result = ProcessAPIResposne(get_income_expenditure(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_profit":
                        api_result = ProcessAPIResposne(get_monthly_profit(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_areawise_deposits":
                        api_result = ProcessAPIResposne(get_areawise_deposits(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_branch_wise_deposits":
                        api_result = ProcessAPIResposne(get_branch_wise_deposits(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_castewise_deposits":
                        api_result = ProcessAPIResposne(get_castewise_deposits(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_member_vs_nonmember_deposits":
                        api_result = ProcessAPIResposne(get_member_vs_nonmember_deposits(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_deposit_categories":
                        api_result = ProcessAPIResposne(get_deposit_categories(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_deposit_interest_rate":
                        api_result = ProcessAPIResposne(get_deposit_interest_rate(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_deposit_volume":
                        api_result = ProcessAPIResposne(get_monthly_deposit_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_deposit_count":
                        api_result = ProcessAPIResposne(get_monthly_deposit_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_closed_deposit_count":
                        api_result = ProcessAPIResposne(get_monthly_closed_deposit_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_closed_deposit_volume":
                        api_result = ProcessAPIResposne(get_monthly_closed_deposit_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_renewed_deposit_count":
                        api_result = ProcessAPIResposne(get_monthly_renewed_deposit_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_renewed_deposit_volume":
                        api_result = ProcessAPIResposne(get_monthly_renewed_deposit_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_branch_wise_loans":
                        api_result = ProcessAPIResposne(get_branch_wise_loans(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_loan_categories":
                        api_result = ProcessAPIResposne(get_loan_categories(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_type_wise_npa_loans":
                        api_result = ProcessAPIResposne(get_type_wise_npa_loans(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_status_wise_npa_loans":
                        api_result = ProcessAPIResposne(get_status_wise_npa_loans(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_type_wise_no_of_loans":
                        api_result = ProcessAPIResposne(get_type_wise_no_of_loans(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_loans_volume":
                        api_result = ProcessAPIResposne(get_monthly_loans_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_loan_interest_rate_distribution":
                        api_result = ProcessAPIResposne(get_loan_interest_rate_distribution(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_loan_recovery_count":
                        api_result = ProcessAPIResposne(get_monthly_loan_recovery_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_loan_recovery_volume":
                        api_result = ProcessAPIResposne(get_monthly_loan_recovery_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_type_wise_transactions_volume":
                        api_result = ProcessAPIResposne(get_type_wise_transactions_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_type_wise_transactions_count":
                        api_result = ProcessAPIResposne(get_type_wise_transactions_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_branch_wise_transactions_volume":
                        api_result = ProcessAPIResposne(get_branch_wise_transactions_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_branch_wise_transactions_count":
                        api_result = ProcessAPIResposne(get_branch_wise_transactions_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_branch_wise_app_users":
                        api_result = ProcessAPIResposne(get_branch_wise_app_users(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_transactions_count":
                        api_result = ProcessAPIResposne(get_monthly_transactions_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_transactions_volume":
                        api_result = ProcessAPIResposne(get_monthly_transactions_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_monthly_pigmy_collection_volume":
                        api_result = ProcessAPIResposne(get_monthly_pigmy_collection_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_online_payments_volume":
                        api_result = ProcessAPIResposne(get_online_payments_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_online_payments_count":
                        api_result = ProcessAPIResposne(get_online_payments_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_online_collections_volume":
                        api_result = ProcessAPIResposne(get_online_collections_volume(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_online_collections_count":
                        api_result = ProcessAPIResposne(get_online_collections_count(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_branch_wise_customers":
                        api_result = ProcessAPIResposne(get_branch_wise_customers(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_caste_wise_customers":
                        api_result = ProcessAPIResposne(get_caste_wise_customers(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_gender_wise_customers":
                        api_result = ProcessAPIResposne(get_gender_wise_customers(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_area_wise_customers":
                        api_result = ProcessAPIResposne(get_area_wise_customers(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_village_wise_customers":
                        api_result = ProcessAPIResposne(get_village_wise_customers(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))
                    elif function_call.name == "get_age_distribution":
                        api_result = ProcessAPIResposne(get_age_distribution(**args, key_bytes=key_bytes, iv_bytes=iv_bytes))                                                                  
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
            if followup_response.usage_metadata:
                print(f"Prompt tokens (input): {followup_response.usage_metadata.prompt_token_count}")
                print(f"Candidates tokens (output): {followup_response.usage_metadata.candidates_token_count}")
                print(f"Total tokens (input + output): {followup_response.usage_metadata.total_token_count}")
            else:
                print("No usage_metadata found in the response.")
            response_tokens = response.usage_metadata.total_token_count if response.usage_metadata else 0
            followup_tokens = followup_response.usage_metadata.total_token_count if followup_response.usage_metadata else 0
            total_tokens = response_tokens + followup_tokens

            return {
            "text": followup_response.candidates[0].content.parts[0].text,
            "total_tokens": total_tokens
            }

        else:
            # ✅ No function call, just return the Gemini text naturally
            for part in parts:
                if hasattr(part, "text") and part.text.strip():
                    return {
            "text": part.text.strip(),
            "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
            }

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
            "Category": category,
            "Value": value,
            "Currency": "INR",
            "Unit": "Lakhs",
        }
        result.append(transformed_item)

    print("\n[API] Transformed result for Gemini:", result)
    return result
