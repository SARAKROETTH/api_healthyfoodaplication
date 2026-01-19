from typing import TypeVar,Generic,Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import hmac
import hashlib

from datetime import datetime ,timedelta
from jose import JWSError,jwt
from fastapi import Depends, Request,HTTPException,status
from fastapi.security import HTTPBearer,HTTPBasicCredentials

load_dotenv()

T = TypeVar('T')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class BaseRepo():

    @staticmethod
    def insert(db:Session,model:Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)
class UserRepo(BaseRepo):

    @staticmethod
    def find_by_username(db:Session,model:Generic[T],username:str):
        return db.query(model).filter(model.username == username).first()
    @staticmethod
    def find_by_number(db: Session,model:Generic[T],number:str):
        return db.query(model).filter(model.phone_number == number).first()


class JWTRepo():
    def generate_token(data: dict,expires_delta: Optional[timedelta]=None):
        to_encode =data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
            to_encode.update({"exp": expire})
            encode_jwt = jwt.encode(to_encode, SECRET_KEY ,algorithm=ALGORITHM)
            return encode_jwt
    def decode_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
            return decode_token if decode_token['expires'] >= datetime.time() else None
        except:
            return None
class OtpRepo():

    @staticmethod
    def generate_otp(phone_number: str, expires_at: datetime) -> str:
        secret = os.getenv("PRIVATE_KEY").encode()

        message = f"{phone_number}:{expires_at.isoformat()}".encode()

        digest = hmac.new(
            secret,
            message,
            hashlib.sha256
        ).digest()  # 🔑 raw bytes

        # Convert bytes → int → 6 digits
        otp_int = int.from_bytes(digest, "big") % 1_000_000

        return f"{otp_int:06d}"


        
