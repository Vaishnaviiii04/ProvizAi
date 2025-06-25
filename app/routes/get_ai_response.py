from flask import Blueprint, request, current_app, make_response
from flask_cors import CORS
import json
import gzip
import io

from app.services.gemini_service import GetPromptResponse
from app.services.encryption_service import EncryptionService
from app.services.db_service import DbService

ai_bp = Blueprint('ai', __name__)
CORS(ai_bp)

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

        extra_meta = {
            "UserId": decrypted_data.get("UserId"),
            "Last_SignedIn_Time": decrypted_data.get("Last_SignedIn_Time"),
            "Bank_Id": decrypted_data.get("Bank_Id"),
            "AppVersion": decrypted_data.get("AppVersion"),
            "Platform": decrypted_data.get("Platform"),
        }

        ai_response = GetPromptResponse(user_input, extra_meta)

        # try:
        #     DbService.log_chat(
        #         user_id= extra_meta["UserId"],
        #         user_input=user_input,
        #         bank_id=extra_meta["Bank_Id"],
        #         platform=extra_meta["Platform"],
        #         response=ai_response
        #     )
        # except Exception as db_err:
        #     print("Failed to log chat to DB:", db_err)
        DbService.log_chat(
                user_id= extra_meta["UserId"],
                user_input=user_input,
                bank_id=extra_meta["Bank_Id"],
                platform=extra_meta["Platform"],
                response=ai_response
            )
        
        response_data["Valid"] = True
        response_data["Message"] = ai_response
    except Exception as db_err:
        print("Failed to log chat to DB:", db_err)
    except json.JSONDecodeError as e:
        response_data["Message"] = f"Invalid JSON format: {e}"
    except ValueError as e:
        response_data["Message"] = str(e)
    except Exception as e:
        response_data["Message"] = f"An unexpected server error occurred: {e}"

    json_output = json.dumps(response_data)
    encrypted_output = EncryptionService(key=key_bytes, iv=iv_bytes).encryptWithAES(json_output)

    accept_encoding = request.headers.get('Accept-Encoding', '')
    if 'gzip' in accept_encoding:
        compressed_data = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode='w') as gz:
            gz.write(encrypted_output.encode('utf-8'))
        compressed_data.seek(0)
        response = make_response(compressed_data.read())
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(encrypted_output)
        response.headers['Content-Type'] = 'application/json'

    return response

@ai_bp.route('/GetAIChat', methods=['GET'])
def get_ai_chat():
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

        extra_meta = {
            "UserId": decrypted_data.get("UserId"),
            "Last_SignedIn_Time": decrypted_data.get("Last_SignedIn_Time"),
            "Bank_Id": decrypted_data.get("Bank_Id"),
            "AppVersion": decrypted_data.get("AppVersion"),
            "Platform": decrypted_data.get("Platform"),
        }

        chats = DbService.get_chats_by_user_id(extra_meta["UserId"])

        response_data["Valid"] = True
        response_data["Message"] = [
            {
                "userInput": row[2],
                "response": row[5]
            } for row in chats
        ]

        # if chats:
        #     response_data["Valid"] = True
        #     response_data["Message"] = [
        #         {
        #             "userInput": row[2],
        #             "response": row[5]
        #         } for row in chats
        #     ]
        # else:
        #     response_data["Message"] = f"No chat found for userId {extra_meta['UserId']}"
    except Exception as db_err:
        print("Failed to log chat to DB:", db_err)
    except json.JSONDecodeError as e:
        response_data["Message"] = f"Invalid JSON format: {e}"
    except ValueError as e:
        response_data["Message"] = str(e)
    except Exception as e:
        response_data["Message"] = f"An unexpected server error occurred: {e}"

    json_output = json.dumps(response_data)
    encrypted_output = EncryptionService(key=key_bytes, iv=iv_bytes).encryptWithAES(json_output)

    accept_encoding = request.headers.get('Accept-Encoding', '')
    if 'gzip' in accept_encoding:
        compressed_data = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode='w') as gz:
            gz.write(encrypted_output.encode('utf-8'))
        compressed_data.seek(0)
        response = make_response(compressed_data.read())
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(encrypted_output)
        response.headers['Content-Type'] = 'application/json'

    return response