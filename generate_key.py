"""
Generate a secure encryption key for bot_id encryption
Run this script to generate a 32-byte key for your .env file
"""
from cryptography.fernet import Fernet
import base64

# Generate a new Fernet key (32 bytes, base64 encoded)
key = Fernet.generate_key()
print("=" * 60)
print("ENCRYPTION_KEY for your .env file:")
print("=" * 60)
print(key.decode())
print("=" * 60)
print("\nCopy this key and paste it into your .env file as ENCRYPTION_KEY")
print("Keep this key secure and never commit it to version control!")

