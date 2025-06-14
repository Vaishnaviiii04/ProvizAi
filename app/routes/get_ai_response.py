from flask import Blueprint, request, jsonify, current_app, make_response
import json
import base64
import gzip
import io

from app.services.gemini_service import GetPromptResponse
from app.services.encryption_service import EncryptionService

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/GetAIResponse', methods=['GET'])
def get_ai_response():
    key_bytes = current_app.config['AES_ENCRYPTION_KEY_STRING'].encode('utf-8')
    iv_bytes = current_app.config['AES_IV_STRING'].encode('utf-8')

    encryption_service = EncryptionService(key=key_bytes, iv=iv_bytes)
    response_data = {"Valid": False, "Message": "An unknown error occurred."}

    try:
        post_data_str = request.args.get('postData')
        if not post_data_str:
            raise ValueError("Missing 'postData' query parameter.")

        post_data_json = json.loads(post_data_str)
        encrypted_val = post_data_json.get('JSONString')
        if not encrypted_val:
            raise ValueError("Missing 'JSONString' field within 'postData'.")

        decrypted_json_string = encryption_service.decryptAes(encrypted_val)
        decrypted_data = json.loads(decrypted_json_string)

        user_input = decrypted_data.get('UserInput')
        if not user_input:
            raise ValueError("Missing 'UserInput' field in decrypted data.")

        # Extract additional metadata
        extra_meta = {
            "UserId": decrypted_data.get("UserId"),
            "Last_SignedIn_Time": decrypted_data.get("Last_SignedIn_Time"),
            "Bank_Id": decrypted_data.get("Bank_Id"),
            "AppVersion": decrypted_data.get("AppVersion"),
            "Platform": decrypted_data.get("Platform"),
        }

        ai_response = GetPromptResponse(user_input, extra_meta)
        response_data["Valid"] = True
        response_data["Message"] = ai_response

    except json.JSONDecodeError as e:
        response_data["Message"] = f"Invalid JSON format: {e}"
    except ValueError as e:
        response_data["Message"] = str(e)
    except Exception as e:
        response_data["Message"] = f"An unexpected server error occurred: {e}"

    json_output = json.dumps(response_data)

    accept_encoding = request.headers.get('Accept-Encoding', '')
    if 'gzip' in accept_encoding:
        compressed_data = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode='w') as gz:
            gz.write(json_output.encode('utf-8'))
        compressed_data.seek(0)
        response = make_response(compressed_data.read())
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(json_output)
        response.headers['Content-Type'] = 'application/json'

    return response