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

        get_income_expenditure_function = {
            "name": "get_income_expenditure",
            "description": "Get income and expenditure data from selected branches.",
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
            "description": "Get monthly profit details from selected branches within a specified date range.",
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
            "description": "Get area-wise deposit data for selected branches and deposit types.",
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
            "description": "Get caste-wise deposit data for selected branches and deposit types.",
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
            "description": "Get member vs non-member deposit data for selected branches and deposit types.",
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
            "description": "Get deposit category-wise data for selected branches and deposit types.",
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
            "description": "Get deposit interest rate data for selected branches and deposit types.",
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
            "description": "Get monthly deposit volume data for selected branches and deposit types.",
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
            "description": "Get monthly deposit count data for selected branches and deposit types.",
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
            "description": "Get monthly closed deposit count data for selected branches and deposit types.",
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
            "description": "Get monthly closed deposit volume data for selected branches and deposit types.",
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
            "description": "Get monthly renewed deposit count data for selected branches and deposit types.",
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
            "description": "Get monthly renewed deposit volume data for selected branches and deposit types.",
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
            "description": "Get branch-wise loan data for selected branches and loan types.",
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
            "description": "Get  loan category-wise data for selected branches and loan types.",
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
            "description": "Get type-wise NPA loan data for selected branches and loan types.",
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
            "description": "Get status-wise NPA loan data for selected branches and loan types.",
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
            "description": "Get type-wise number of loan data for selected branches and loan types.",
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
            "description": "Get monthly loans volume data for selected branches and loan types.",
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
            "description": "Get loan interest rate distribution data for selected branches and loan types.",
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
            "description": "Get monthly loan recovery count data for selected branches and loan types.",
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
            "description": "Get monthly loan recovery volume data for selected branches and loan types.",
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
            "description": "Get type-wise transaction volume data for selected branches within a date range.",
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
            "description": "Get type-wise transaction count data for selected branches within a date range.",
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
            "description": "Get branch-wise transactions volume data for selected branches within a date range.",
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
            "description": "Get branch-wise transactions count data for selected branches within a date range.",
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
            "description": "Get branch-wise app user data for selected branches within a date range.",
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
            "description": "Get monthly transactions count data for selected branches within a date range.",
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
            "description": "Get monthly transactions volume data for selected branches within a date range.",
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
            "description": "Get monthly pigmy collection volume data for selected branches within a date range.",
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
            "description": "Get monthly online payments volume data for selected branches within a date range.",
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
            "description": "Get monthly online payments count data for selected branches within a date range.",
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
            "description": "Get monthly online collections volume data for selected branches within a date range.",
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
            "description": "Get monthly online collections count data for selected branches within a date range.",
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
            "description": "Get branch wise customers data for selected branches within a date range.",
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
            "description": "Get caste wise customers data for selected branches within a date range.",
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
            "description": "Get gender wise customers data for selected branches within a date range.",
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
            "description": "Get area wise customers data for selected branches within a date range.",
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
            "description": "Get village wise customers data for selected branches within a date range.",
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
            "description": "get age distribution data for selected branches within a date range.",
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
            model="gemini-2.0-flash-lite",
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
            "Category": category,
            "Value": value,
            "Currency": "INR",
            "Unit": "Lakhs",
        }
        result.append(transformed_item)

    print("\n[API] Transformed result for Gemini:", result)
    return result