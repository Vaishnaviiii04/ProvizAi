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
#======= Get Revenue Data =========
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

#======= Income Expenditure ========
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
    
#======== Monthly Profit ===========
def get_monthly_profit(
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
        url = BASE_URL + "GetMonthlyProfit?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#===== DEPOSITS ======
#====== Branchwise deposits =======
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

#====== Areawise deposits ========
def get_areawise_deposits(
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
        url = BASE_URL + "GetAreaWiseDeposits?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#===== CasteWise Deposits =======
def get_castewise_deposits(
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
        url = BASE_URL + "GetCasteWiseDeposits?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Member vs Non Member deposits =======
def get_member_vs_nonmember_deposits(
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
        url = BASE_URL + "GetMembervsNonMemberDeposits?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#===== Deposit Categories ======
def get_deposit_categories(
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
        url = BASE_URL + "GetDepositCategories?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
    
#===== Deposit Interest Rate =======
def get_deposit_interest_rate(
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
        url = BASE_URL + "GetDepositInterestRate?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Monthly Deposit Volume ========
def get_monthly_deposit_volume(
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
        url = BASE_URL + "GetMonthlyDepositVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#======== Monthly Deposit Count ========
def get_monthly_deposit_count(
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
        url = BASE_URL + "GetMonthlyDepositCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Monthly closed Deposit count =======
def get_monthly_closed_deposit_count(
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
        url = BASE_URL + "GetMonthlyClosedDepositCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#======= Get Monthly closed deposit volume ======
def get_monthly_closed_deposit_volume(
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
        url = BASE_URL + "GetMonthlyClosedDepositVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Monthly Renewed Deposit Count =======
def get_monthly_renewed_deposit_count(
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
        url = BASE_URL + "GetMonthlyRenewedDepositCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
    
#======= Monthly Renewed Deposit Volume ======
def get_monthly_renewed_deposit_volume(
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
        url = BASE_URL + "GetMonthlyRenewedDepositVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#======= LOANS =======
#======= Branchwise Loans =======
def get_branch_wise_loans(
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
        url = BASE_URL + "GetBranchWiseLoans?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Loan Categories =======
def get_loan_categories(
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
        url = BASE_URL + "GetLoanCategories?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#===== Type Wise NPA Loan =======
def get_type_wise_npa_loans(
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
        url = BASE_URL + "GetTypeWiseNPALoans?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Status wise Npa Loans =====
def get_status_wise_npa_loans(
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
        url = BASE_URL + "GetStatusWiseNPALoans?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Type wise No of Loans ======
def get_type_wise_no_of_loans(
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
        url = BASE_URL + "GetTypeWiseNoofLoans?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
    
#===== Monthly Loans Volume ======
def get_monthly_loans_volume(
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
        url = BASE_URL + "GetMonthlyLoansVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#======= Loan Interest Rate Distribution =======
def get_loan_interest_rate_distribution(
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
        url = BASE_URL + "GetLoanInterestRateDistribution?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Monthly loan recovery count =====
def get_monthly_loan_recovery_count(
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
        url = BASE_URL + "GetMonthlyLoanRecoveryCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Monthly loan recovery volume ======
def get_monthly_loan_recovery_volume(
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
        url = BASE_URL + "GetMonthlyLoanRecoveryVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
    
#====== TRANSACTION =======
#====== Type wise Transaction Volume ======
def get_type_wise_transactions_volume(
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
        url = BASE_URL + "GetTypeWiseTransactionsVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
    
#======== Type wise Tranction Count ========
def get_type_wise_transactions_count(
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
        url = BASE_URL + "GetTypeWiseTransactionsCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Branch wise Transaction Volume ======    
def get_branch_wise_transactions_volume(
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
        url = BASE_URL + "GetBranchWiseTransactionsVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Branch wise Transaction Count ======    
def get_branch_wise_transactions_count(
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
        url = BASE_URL + "GetBranchWiseTransactionsCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Branch wise App Users ======    
def get_branch_wise_app_users(
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
        url = BASE_URL + "GetBranchWiseAppUsers?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Monthly Transactions Count ======    
def get_monthly_transactions_count(
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
        url = BASE_URL + "GetMonthlyTransactionsCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
#====== Monthly Transactions Volume ======
def get_monthly_transactions_volume(
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
        url = BASE_URL + "GetMonthlyTransactionsVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Monthly Pigmy Collection Volume ======
def get_monthly_pigmy_collection_volume(
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
        url = BASE_URL + "GetMonthlyPigmyCollectionVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Online Payments Volume ======
def get_online_payments_volume(
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
        url = BASE_URL + "GetOnlinePaymentsVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Online Payments Count ======
def get_online_payments_count(
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
        url = BASE_URL + "GetOnlinePaymentsCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Online Collections Volume ======
def get_online_collections_volume(
    selectedBranches=None, fromMonth=None, fromYear=None,
    toMonth=None, toYear=None, UserId=None, Last_SignedIn_Time=None,
    Bank_Id=None, AppVersion=None, Platform=None,
    key_bytes=None, iv_bytes=None
):
    try:
        # Fallback to app config if key/iv not provided
        key_bytes = key_bytes or current_app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
        iv_bytes = iv_bytes or current_app.config['AES_IV_STRING'].encode('utf-8')

        # Prepare encrypted payload
        post_data = _prepare_common_payload(
            selectedBranches, fromMonth, fromYear, toMonth, toYear,
            UserId, Last_SignedIn_Time, Bank_Id, AppVersion, Platform
        )

        encrypted_val = EncryptionService(key=key_bytes, iv=iv_bytes).encryptWithAES(json.dumps(post_data))
        
        # Compose request
        url = BASE_URL + "GetOnlineCollectionsVolume?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        # Check response status
        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        # Decrypt and parse data
        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#====== Online Collections Count ======
def get_online_collections_count(
    selectedBranches=None, fromMonth=None, fromYear=None,
    toMonth=None, toYear=None, UserId=None, Last_SignedIn_Time=None,
    Bank_Id=None, AppVersion=None, Platform=None,
    key_bytes=None, iv_bytes=None
):
    try:
        # AES key/iv from Flask config if not explicitly passed
        key_bytes = key_bytes or current_app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
        iv_bytes = iv_bytes or current_app.config['AES_IV_STRING'].encode('utf-8')

        # Prepare encrypted payload
        post_data = _prepare_common_payload(
            selectedBranches, fromMonth, fromYear, toMonth, toYear,
            UserId, Last_SignedIn_Time, Bank_Id, AppVersion, Platform
        )

        encrypted_val = EncryptionService(key=key_bytes, iv=iv_bytes).encryptWithAES(json.dumps(post_data))
        
        # Make GET request to the endpoint
        url = BASE_URL + "GetOnlineCollectionsCount?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        # Return error if failed
        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        # Decrypt the response
        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#======= Customers =======    
#==== Branch wise Customers======

def get_branch_wise_customers(
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

        url = BASE_URL + "GetBranchWiseCustomers?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#======= caste wise Customers==========

def get_caste_wise_customers(
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

        url = BASE_URL + "GetCasteWiseCustomers?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
    
#====== Gender wise Customers ======     

def get_gender_wise_customers(
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

        url = BASE_URL + "GetGenderWiseCustomers?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#==  Area wise Customers =======
def get_area_wise_customers(
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

        url = BASE_URL + "GetAreaWiseCustomers?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}

#===== Village wise Customer =======

def get_village_wise_customers(
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

        url = BASE_URL + "GetVillageWiseCustomers?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
    
#====== Age Distribution ========

def get_age_distribution(
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

        url = BASE_URL + "GetAgeDistribution?postData=" + json.dumps({"JSONString": encrypted_val})
        response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)

        if response.status_code != 200:
            return {"error": f"API returned {response.status_code}"}

        decrypted_json = EncryptionService(key=key_bytes, iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
        return json.loads(decrypted_json)

    except Exception as e:
        return {"error": f"API call failed: {e}"}
