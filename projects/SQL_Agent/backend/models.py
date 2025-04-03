from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    otp = Column(String)
    otp_created_on = Column(TIMESTAMP)

