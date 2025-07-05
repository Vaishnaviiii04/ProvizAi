# ==================== function_service.py ====================

from flask import json, current_app
import requests
from app.services.encryption_service import EncryptionService

BASE_URL = "http://13.234.167.225:63580/CBS_DASHBOARD/api/v1/"

def _prepare_common_payload(selectedBranches, fromMonth, fromYear, toMonth, toYear,
                             UserId, Last_SignedIn_Time, Bank_Id, AppVersion, Platform):
    return {
        "selectedbranches": (
            selectedBranches if isinstance(selectedBranches, str)
            else ",".join(selectedBranches) if selectedBranches else None
        ),
        "fromMonth": fromMonth,
        "fromYear": fromYear,
        "toMonth": toMonth,
        "toYear": toYear,
        "UserId": UserId,
        "Last_SignedIn_Time": Last_SignedIn_Time,
        "Bank_Id": Bank_Id,
        "AppVersion": AppVersion,
        "Platform": Platform,
    }

def get_revenue_sources(
    selectedBranches=None, fromMonth=None, fromYear=None,
    toMonth=None, toYear=None, UserId=None, Last_SignedIn_Time=None,
    Bank_Id=None, AppVersion=None, Platform=None,
    key_bytes=None, iv_bytes=None
):
    try:
        key_bytes = key_bytes or current_app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
        iv_bytes = iv_bytes or current_app.config['AES_IV_STRING'].encode('utf-8')

        post_data = _prepare_common_payload(
            selectedBranches, fromMonth, fromYear, toMonth, toYear,
            UserId, Last_SignedIn_Time, Bank_Id, AppVersion, Platform
        )

        encrypted_val = EncryptionService(key=key_bytes, iv=iv_bytes).encryptWithAES(json.dumps(post_data))
        url = BASE_URL + "GetRevenueSources?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

def get_income_expenditure(
    selectedBranches=None, fromMonth=None, fromYear=None, toMonth=None, toYear=None,
    UserId=None, Last_SignedIn_Time=None, Bank_Id=None, AppVersion=None, Platform=None,
    key_bytes=None, iv_bytes=None
):
    try:
        key_bytes = key_bytes or current_app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
        iv_bytes = iv_bytes or current_app.config['AES_IV_STRING'].encode('utf-8')

        post_data = _prepare_common_payload(
            selectedBranches, fromMonth, fromYear, toMonth, toYear,
            UserId, Last_SignedIn_Time, Bank_Id, AppVersion, Platform
        )

        encrypted_val = EncryptionService(key=key_bytes, iv=iv_bytes).encryptWithAES(json.dumps(post_data))
        url = BASE_URL + "GetIncomeExpenditure?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

def get_branch_wise_deposits(
    selectedBranches=None, selectedTypes=None, fromMonth=None, fromYear=None,
    toMonth=None, toYear=None, UserId=None, Last_SignedIn_Time=None,
    Bank_Id=None, AppVersion=None, Platform=None,
    key_bytes=None, iv_bytes=None
):
    try:
        key_bytes = key_bytes or current_app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
        iv_bytes = iv_bytes or current_app.config['AES_IV_STRING'].encode('utf-8')

        post_data = _prepare_common_payload(
            selectedBranches, fromMonth, fromYear, toMonth, toYear,
            UserId, Last_SignedIn_Time, Bank_Id, AppVersion, Platform
        )
        post_data["selectedtypes"] = (
            selectedTypes if isinstance(selectedTypes, str)
            else ",".join(selectedTypes) if selectedTypes else None
        )

        encrypted_val = EncryptionService(key=key_bytes, iv=iv_bytes).encryptWithAES(json.dumps(post_data))
        url = BASE_URL + "GetBranchWiseDeposits?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

