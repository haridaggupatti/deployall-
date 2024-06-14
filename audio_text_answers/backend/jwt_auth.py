import jwt
from decouple import config
import logging

# Setup logging
logger = logging.getLogger(__name__)

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

def token_resp(token: str):
    return {
        "access_token": token
    }

def signJWT(userId: str):
    try:
        user_id = userId.decode()
    except AttributeError:
        user_id = userId

    payload = {
        "userId": user_id
    }

    try:
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return "Bearer " + token
    except Exception as e:
        logger.error(f"Error signing JWT: {str(e)}")
        raise Exception("Error signing JWT")

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return {"error": "Invalid token"}
    except Exception as e:
        logger.error(f"Error decoding JWT: {str(e)}")
        return {"error": "Error decoding token"}
