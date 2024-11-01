from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


    @field_validator('first_name', 'last_name', 'password')
    @classmethod
    def no_empty_strings(cls, v):
        if not v.strip():
            raise ValueError('This field cannot be empty')
        return v

    @field_validator('first_name', 'last_name', 'password', 'email')
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AutoReply(BaseModel):
    auto_reply_delay: int

