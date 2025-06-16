import random

from flask import json, current_app
import requests


from app.services.encryption_service import EncryptionService



def get_revenue_sources(selectedBranches, fromMonth=None, fromYear=None, toMonth=None, toYear=None):
    range_parts = []
    if fromMonth: range_parts.append(fromMonth)
    if fromYear: range_parts.append(fromYear)
    if toMonth or toYear:
        range_parts.append("to")
        if toMonth: range_parts.append(toMonth)
        if toYear: range_parts.append(toYear)
    date_range = " ".join(range_parts) if range_parts else "unspecified"
    total = random.randint(700000, 2000000)
    formatted_total = f"\u20b9{total:,}"
    return {
        "selectedBranches": selectedBranches,
        "period": date_range,
        "revenue_data": [
            {"category": "Jewel Loan", "percentage": random.choice([25, 30, 35])},
            {"category": "Savings", "percentage": random.choice([40, 45, 50])},
            {"category": "Current", "percentage": random.choice([15, 20, 25])}
        ],
        "total_revenue": formatted_total
    }

def get_branch_wise_deposits(selectedBranches, selectedTypes=None, fromMonth=None, fromYear=None, toMonth=None, toYear=None, UserId=None, Last_SignedIn_Time=None, Bank_Id=None, AppVersion=None, Platform=None):
    key_bytes = current_app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
    iv_bytes = current_app.config['AES_IV_STRING'].encode('utf-8')
    API_URL = "http://172.16.30.43:8080/CL_LOANAPI/api/v1/GetBranchWiseDeposits"
    if API_URL:
        try:
            post_data = {
                "selectedbranches": selectedBranches if isinstance(selectedBranches, str) else ",".join(selectedBranches),
                "selectedtypes": selectedTypes if isinstance(selectedTypes, str) else ",".join(selectedTypes or []),
                "fromMonth": fromMonth or None,
                "fromYear": fromYear or None,
                "toMonth": toMonth or None,
                "toYear": toYear or None,
                "UserId": UserId or None,
                "Last_SignedIn_Time": Last_SignedIn_Time or None,
                "Bank_Id": Bank_Id or None,
                "AppVersion":AppVersion or None,
                "Platform": Platform or None,
            }
            encrypted_val = EncryptionService(key=key_bytes,iv=iv_bytes).encryptWithAES(json.dumps(post_data))
            url = f"{API_URL}?postData=" + json.dumps({"JSONString": encrypted_val})
            response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=10)
            # decompressed = gzip.decompress(response.content)
            decrypted_json = EncryptionService(key=key_bytes,iv=iv_bytes).decryptAes(response.content.decode("utf-8"))
            return json.loads(decrypted_json)
        except Exception as e:
            return {"error": f"API call failed: {e}"}
    branches = selectedBranches.split(",")
    types = selectedTypes.split(",") if selectedTypes else ["Savings", "Current", "Loan"]
    date_range = f"{fromMonth or ''} {fromYear or ''} to {toMonth or ''} {toYear or ''}".strip()
    #doughnut_data = [{"branch": b.strip(), "deposits": random.randint(10000, 80000)} for b in branches]
   