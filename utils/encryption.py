from cryptography.fernet import Fernet
import base64
from config import Config

def _get_fernet():
    """Get Fernet instance from encryption key"""
    key = Config.ENCRYPTION_KEY
    if isinstance(key, bytes):
        key = key.decode()
    # Ensure it's a valid Fernet key (32 bytes base64 encoded)
    try:
        # Try to use the key directly
        return Fernet(key.encode() if isinstance(key, str) else key)
    except:
        # If key is not valid, generate a new one (shouldn't happen in production)
        raise ValueError("Invalid encryption key. Please generate a new key using generate_key.py")

def encrypt_bot_id(bot_id: str) -> str:
    """Encrypt bot_id before storing in database"""
    fernet = _get_fernet()
    encrypted = fernet.encrypt(bot_id.encode())
    return encrypted.decode()

def decrypt_bot_id(encrypted_bot_id: str) -> str:
    """Decrypt bot_id from database"""
    from cryptography.fernet import InvalidToken
    
    try:
        fernet = _get_fernet()
        decrypted = fernet.decrypt(encrypted_bot_id.encode())
        return decrypted.decode()
    except InvalidToken:
        # If decryption fails, return a placeholder indicating encryption key mismatch
        return "[Encrypted - Key Mismatch]"
    except Exception as e:
        # Handle other decryption errors gracefully
        return f"[Decryption Error: {type(e).__name__}]"
