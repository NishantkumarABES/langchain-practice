from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


class RequestOtp(BaseModel):
    username: str
    email: str

class VerifyOtp(BaseModel):
    username: str
    otp: str


class ProcessFile(BaseModel):
    file_id: str
    file_name: str
    file_type: str



class UserInput(BaseModel):
    file_id: str
    file_type: str
    question: str