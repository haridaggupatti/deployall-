from fastapi import APIRouter, HTTPException, responses
from models import *
from mongo import *
import hashlib
import random
import smtplib
from email.message import EmailMessage
import uuid
from jwt_auth import *
import logging

router = APIRouter(prefix='/api/users')
logger = logging.getLogger(__name__)

@router.post("/register", tags=['user'])
async def user_register(data: register_params):
    redis_client = None
    try:
        redis_client = await redisConnection()
        temp_mail = redis_client.setex(f"{data.email}_email", 3000, data.email)
        temp_username = redis_client.setex(f"{data.email}_username", 3000, data.username)
        hash_temp_password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
        temp_password = redis_client.setex(f"{data.email}_password", 3000, hash_temp_password)

        collection = await dbconnect('user_auth', 'users')
        res = collection.find_one({"email": data.email})
        if res:
            raise HTTPException(status_code=400, detail="User already exists")

        await send_otp(redis_client.get(f"{data.email}_email").decode())
        return {"msg": "Details stored in Redis"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if redis_client:
            redis_client.close()

@router.post("/send_otp", tags=["OTP"])
async def send_otp(request: otp_email):
    try:
        email = request.email
        otp_generated = random.randint(10000, 99999)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("your_email@example.com", "your_password")

        message = EmailMessage()
        message["From"] = "your_email@example.com"
        message["To"] = email
        message["Subject"] = "Verification code to change password"
        message.set_content(f"Your verification code is {otp_generated}")

        s.send_message(message)
        s.quit()
        await redis_store(otp_generated, email)
        return {"msg": "Mail sent successfully"}
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def redis_store(otp, email):
    redis_client = None
    try:
        redis_client = await redisConnection()
        key = f"{email}_otp"
        redis_client.setex(key, 3000, otp)
    except Exception as e:
        logger.error(f"Error storing OTP in Redis: {str(e)}")
    finally:
        if redis_client:
            redis_client.close()

@router.post('/verify_otp', tags=['OTP'])
async def verify_otp(data: only_otp):
    redis_client = None
    try:
        redis_client = await redisConnection()
        stored_otp = redis_client.get(f"{data.email}_otp")
        if stored_otp is None:
            raise HTTPException(status_code=404, detail="OTP not found")

        stored_otp = stored_otp.decode()
        if data.otp != stored_otp:
            raise HTTPException(status_code=401, detail="Invalid OTP")

        email_id = redis_client.get(f"{data.email}_email").decode()
        user_name = redis_client.get(f"{data.email}_username").decode()
        user_password = redis_client.get(f"{data.email}_password").decode()

        collection = await dbconnect('user_auth', 'users')
        user_data = {
            "email": email_id,
            "name": user_name,
            "password": user_password
        }
        collection.insert_one(user_data)
        return {"msg": "User created successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during OTP verification: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if redis_client:
            redis_client.close()

async def check_user(data):
    try:
        password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
        collection = await dbconnect('user_auth', 'users')
        result = collection.find_one({"email": data.email})
        return result and result.get("password") == password
    except Exception as e:
        logger.error(f"Error checking user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post('/login', tags=['Authentication'])
async def user_login(data: login_params):
    try:
        if await check_user(data):
            access_token = signJWT(data.email)
            response = responses.JSONResponse({"status": "Logged in Successfully", "access_token": access_token})
            response.set_cookie("access_token", str(uuid.uuid4()), path="/", expires=3600, samesite="Lax", secure=True)
            return response
        else:
            raise HTTPException(status_code=401, detail="Wrong Credentials")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post('/forgot-password', tags=['Authentication'])
async def forgot_password(data: forgotPassword_params):
    redis_client = None
    try:
        redis_client = await redisConnection()
        stored_otp = redis_client.get(f"{data.email}_otp")
        if stored_otp is None or stored_otp.decode() != data.otp:
            raise HTTPException(status_code=401, detail="Incorrect OTP")

        if data.newpassword != data.confirm_Password:
            raise HTTPException(status_code=401, detail="New Password and confirmation do not match")

        collection = await dbconnect('user_auth', 'users')
        result = collection.find_one({"email": data.email})
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        new_password = hashlib.md5(data.newpassword.encode('utf-8')).hexdigest()
        collection.update_one({"_id": result.get("_id")}, {'$set': {"password": new_password}})
        return {"msg": "Password Updated Successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if redis_client:
            redis_client.close()

@router.post('/reset-password', tags=['Authentication'])
async def reset_password(data: resetPassword_params):
    try:
        collection = await dbconnect('user_auth', 'users')
        result = collection.find_one({"email": data.email})
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        old_password = result.get("password")
        user_entered_password = hashlib.md5(data.old_password.encode('utf-8')).hexdigest()
        if old_password != user_entered_password:
            raise HTTPException(status_code=401, detail="Incorrect old password")

        if data.new_password != data.confirm_password:
            raise HTTPException(status_code=401, detail="New Password and confirmation do not match")

        new_pass = hashlib.md5(data.new_password.encode('utf-8')).hexdigest()
        collection.update_one({"_id": result.get("_id")}, {'$set': {"password": new_pass}})
        return {"msg": "Password Updated Successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
