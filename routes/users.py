from fastapi import APIRouter,Depends,HTTPException
from schemas.users import ResponeSchema,Resister,TokenRespone,Login,RequestOtp,OTPRespone,Verify_Otp
from sqlalchemy.orm import Session
from config import get_db
from passlib.context import CryptContext
from repository.users import UserRepo,JWTRepo,OtpRepo
from models.users import Users
from fastapi.responses import JSONResponse

from models.user_otp import OTP

from utils.otp import generate_otp,hash_otp,verify_code


from datetime import datetime, timedelta



router = APIRouter(
    tags={"Authentication"},
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"   # ✅ CORRECT
)



@router.post("/request-otp")
async def request_otp(request: RequestOtp,db: Session =Depends(get_db)):
    otp = generate_otp()

    number = request.phone_number

    otp_record = (
        db.query(OTP)
        .filter(OTP.phone_number == request.phone_number)
        .first()
    )

    if otp_record:
        db.delete(otp_record)
        db.commit

    otp_has = hash_otp(otp=otp)

    expires_at = datetime.utcnow() + timedelta(minutes=1)

    otp_entry = OTP(
        phone_number = request.phone_number,
        otp_code = otp_has,
        expires_at = expires_at
    )
    
    db.add(otp_entry)
    db.commit()

    # Send OTP via SMS in production; for now just print
    print(f"OTP for {number}: {otp}")

    return {"message": "OTP generated successfully", "expires_at": expires_at.isoformat()}

@router.post("/verify-otp")
async def verify_otp(request: Verify_Otp,db: Session = Depends(get_db)):

    otp_has = hash_otp(request.otp)

    otp_record = (
        db.query(OTP)
        .filter(OTP.phone_number == request.phone_number)
        .first()
    )

    verify = verify_code(plain_otp=request.otp,hashed_otp=otp_record.otp_code)

    if not verify:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if otp_record.expires_at < datetime.utcnow():
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    db.delete(otp_record)
    db.commit()

    return {"message": "OTP verified successfully"}

