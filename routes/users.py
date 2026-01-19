from fastapi import APIRouter,Depends,HTTPException
from schemas.users import ResponeSchema,Resister,TokenRespone,Login,RequestOtp,OTPRespone,Verify_Otp
from sqlalchemy.orm import Session
from config import get_db
from passlib.context import CryptContext
from repository.users import UserRepo,JWTRepo,OtpRepo
from models.users import Users
from fastapi.responses import JSONResponse

from utils.otp import hash_otp

from datetime import datetime,timedelta,timezone


router = APIRouter(
    tags={"Authentication"},
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"   # ✅ CORRECT
)

# register
@router.post("/signup")
async def signup(request: Resister,db: Session = Depends(get_db)):
    try:
        # create data input
        _user = Users(
            username = request.username,
            phone_number = request.phone_number,
            image_url = request.image_url,
            country_code = request.country_code)
        # for insert to database 
        UserRepo.insert(db,_user)
        return ResponeSchema(code="200",status="Ok",message="Success save data" ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponeSchema(code="500",status="Error",message="Internal Server Error").dict(exclude_none=True)


@router.post("/login")
async def login(request: Login, db: Session = Depends(get_db)):
    try:
        _user = UserRepo.find_by_number(db, Users, request.phone_number)

        if not _user:

            return JSONResponse(
                status_code=404,
                content= ResponeSchema(
                code="404",
                status="Error",
                message="USER_NOT_FOUND"
            ).dict(exclude_none=True)
            )

        if _user.otp_expires_at is None or _user.otp_expires_at < datetime.utcnow():
            return JSONResponse(
                status_code=402,
                content= ResponeSchema(
                code="402",
                status="Error",
                message="OTP_EXPIRED"
            ).dict(exclude_none=True)
            )

        if not pwd_context.verify(request.otp, _user.otp_hash):
            return JSONResponse(
                status_code=401,
                content= ResponeSchema(
                code="401",
                status="Error",
                message="INVALID_OTP"
            ).dict(exclude_none=True)
            )

        # clear OTP
        _user.otp_hash = None
        _user.otp_expires_at = None
        db.commit()

        token = JWTRepo.generate_token({"sub": str(_user.id)})

        return ResponeSchema(
            code="200",
            status="Ok",
            message="LOGIN_SUCCESS",
            result=TokenRespone(
                access_token=token,
                token_type="bearer"
            ).dict(exclude_none=True)
        ).dict(exclude_none=True)

    except Exception as error:
        print(error)
        return JSONResponse(status_code=500,content=ResponeSchema(code="500",status="Error",message="Internal Server Error").dict(exclude_none=True))


@router.post("/request-otp")
def request_otp(request: RequestOtp,db: Session = Depends(get_db)):
    user = UserRepo.find_by_number(db, Users, request.phone_number)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp = OtpRepo.generate_otp(user.id, expires_at)

    otp_hash = hash_otp(otp=otp)
    user.otp_hash = otp_hash
    user.otp_expires_at = expires_at
    user.country_code = request.country_code
    db.commit()
    db.refresh(user)


    # try:
    #     send_otp(
    #         code_country=user.country_code,
    #         phone_number=user.phone_number,
    #         otp=otp
    #     )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Failed to send OTP")

    print(f"{otp} is {expires_at} the has {otp_hash}")

    return ResponeSchema(
        code="200",
        status="OK",
        message="OTP_SENT",
        result={
            "request_otp_status": True,
        }
    )

@router.post("/verify-otp")
async def verify_otp(request: Verify_Otp ,db:Session =Depends(get_db) ):
        
        _user = UserRepo.find_by_number(db=db, model=Users,number=request.phone_number)

        # Find user
        if not _user:
            raise HTTPException(
                status_code=404,
                detail=" user not founded "
            )
        
        # Check OTP expiry
        if not _user.otp_hash or not _user.otp_expires_at:
            raise HTTPException(status_code=400, detail="No OTP requested")
        
        if datetime.utcnow() > _user.otp_expires_at:
        # Clear expired OTP
            _user.otp_hash = None
            _user.otp_expires_at = None
            db.commit()
            raise HTTPException(status_code=400, detail="OTP expired")
        
        if _user.otp_hash != hash_otp(request.otp):
            raise HTTPException(status_code=400, detail="Invalid OTP")
            
        
        #OTP verified: clear from DB
        _user.otp_hash = None
        _user.otp_expires_at = None
        db.commit()

        return ResponeSchema(
            code="200",
            status="OK",
            message="OTP verified successfully",
            result={
            "phone_number": _user.phone_number,
            "role": _user.role.value
            }
        )
        