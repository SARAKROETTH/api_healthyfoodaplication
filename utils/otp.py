import os
import hashlib

from dotenv import load_dotenv

load_dotenv()

def hash_otp(otp: str) ->str:
    _secret = os.getenv("PRIVATE_KEY")
    return hashlib.sha256(
        f"{otp}{_secret}".encode()
    ).hexdigest()
