import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

# Pass KEY and IV during initialization or from current_app.config

class EncryptionService:
    def __init__(self, key: bytes, iv: bytes):
        if len(key) != 32: # Enforce 32-byte key for AES-256
            raise ValueError("Key must be 32 bytes for AES-256 encryption.")
        if len(iv) != 16: # Enforce 16-byte IV
            raise ValueError("IV must be 16 bytes.")
        self.key = key
        self.iv = iv

    def decryptAes(self, base64_encrypted_text: str) -> str:
        try:
            processed_base64_text = base64_encrypted_text.replace(' ', '+')
            encrypted_bytes = base64.b64decode(processed_base64_text.encode('utf-8'))
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted_padded_bytes = cipher.decrypt(encrypted_bytes)
            decrypted_bytes = unpad(decrypted_padded_bytes, AES.block_size)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {e}. Check key, IV, padding, and input format.")

    def encryptWithAES(self, plaintext: str) -> str:
        try:
            padded_bytes = pad(plaintext.encode('utf-8'), AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            encrypted_bytes = cipher.encrypt(padded_bytes)
            return base64.b64encode(encrypted_bytes).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to encrypt data: {e}.")