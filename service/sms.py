import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client =Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_otp(code_country:str, phone_number: str ,otp: str):
    message = client.messages.create(
        body=f"Your OTP is {otp}. It expires in 5 minutes.",
        from_=os.getenv("TWILIO_PHONE"),
        to=f"{code_country}{phone_number}"
    )
    return message.sid