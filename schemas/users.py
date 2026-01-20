from typing import Generic,Optional,TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel

T =TypeVar('T')

# login
class Login(BaseModel):
    phone_number:str

class RequestOtp(BaseModel):
    country_code:str
    phone_number:str

class Verify_Otp(BaseModel):
    phone_number:str
    otp: str
    
# register
class Resister(BaseModel):
    username : str
    phone_number:str
    image_url: str
    country_code: str


class ResponeSchema(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T] = None
    expires_at: str = None


class TokenRespone(BaseModel):
    access_token: str
    token_type: str

class OTPRespone(BaseModel):
    message: str
    phone_number: str
    otp: str

class ResenOtp(BaseModel):
    phone_number: str
    country_code: str
