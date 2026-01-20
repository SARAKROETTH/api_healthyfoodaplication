# Helper function to generate OTP
import random
import bcrypt


def generate_otp():
    return str(random.randint(1000, 9999))



def hash_otp(otp: str) -> str:
    return bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode()


import bcrypt

def verify_code(plain_otp: str, hashed_otp: str) -> bool:
    return bcrypt.checkpw(
        plain_otp.encode(),
        hashed_otp.encode()
    )

