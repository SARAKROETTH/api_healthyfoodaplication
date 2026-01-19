import enum
import datetime
from sqlalchemy import Column,Integer,String ,Boolean , DateTime,Enum
from config import Base

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    image_url = Column(String)
    country_code = Column(String, nullable=False)

    role = Column(
        Enum(UserRole, name="user_role"),
        default=UserRole.user,
        nullable=False
    )

    otp_hash = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
