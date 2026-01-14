from datetime import datetime, timedelta
from uuid import uuid4
import jwt
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.config import security_settings

_serializer = URLSafeTimedSerializer(security_settings.JWT_SECRET)

# generate JWT access token
token = _serializer.dumps({"email": "roshan9tiwari@gmail.com"})

# decode JWT access token
token_data = _serializer.loads(token, max_age=timedelta(days=1).total_seconds())  # Token valid for 1 hour


def generate_access_token(
        data:dict, expires:timedelta= timedelta(days=1)
) -> str:
    return jwt.encode(
        payload={
                  **data,  
                # jti = JWT ID for uniquely identifying the token
                "jti": uuid4().hex,    
                "exp": datetime.now() + expires,
        },
            algorithm=security_settings.JWT_ALGORITHM,
            key=security_settings.JWT_SECRET  
        )
        

def decode_access_token(token:str) -> dict:
    try:
        return  jwt.decode(
        jwt = token,
        algorithms=[security_settings.JWT_ALGORITHM],
        key=security_settings.JWT_SECRET
        )
    except jwt.PyJWTError:
        return None 
    
def generate_url_token(
        data:dict
) -> str:
    return _serializer.dumps(data)

def decode_url_token(
        token:str,
        expiry:timedelta | None = None # default 1 hour
) -> dict | None:
    try:
        return _serializer.loads(token, max_age=expiry.total_seconds() if expiry else None )
    except (BadSignature, SignatureExpired):
        return None