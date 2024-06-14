import pydantic
from pydantic import EmailStr, constr

class register_params(pydantic.BaseModel):
    username: str = pydantic.Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: constr(min_length=8)

class otp_email(pydantic.BaseModel):
    email: EmailStr

class only_otp(pydantic.BaseModel):
    otp: constr(min_length=5, max_length=5)
    email: EmailStr

class login_params(pydantic.BaseModel):
    email: EmailStr
    password: str

class forgotPassword_params(pydantic.BaseModel):
    email: EmailStr
    otp: constr(min_length=5, max_length=5)
    newpassword: constr(min_length=8)
    confirm_Password: constr(min_length=8)

class resetPassword_params(pydantic.BaseModel):
    email: EmailStr
    old_password: str
    new_password: constr(min_length=8)
    confirm_password: constr(min_length=8)

class prompt_text(pydantic.BaseModel):
    user_id: str
    prompt_text: str
    resume_context: str
    resume_prompt: str
