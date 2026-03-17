from typing import Dict, Any
from jose import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from app.config.constant import config


class ReturnToken(BaseModel):
    access_token: str
    refresh_token: str
    token_expiration_date: datetime

#1. get user id(required), access_token_id and refresh_token_id(required) and is email(optional)
#2. generate tokens
#3. return access_token and refresh_token

async def generate_token(userData: Dict[str, Any]) -> ReturnToken:
    # get expireation time from config
    days_to_add = int(config['TOKEN_EXPIRATION_TIME'])
    # get token secret from config
    token_secret_key = config['TOKEN_SECRET']
    # get algorithem type from config
    algorithm = config['ALGORITHM']
    # generate expires time 
    expires = datetime.now(timezone.utc) + timedelta(days=days_to_add)
    
    # access payload generate
    access_payload: Dict[str, Any] = {
        "id": userData['access_token_id'],
        "userId": userData['user_id'],
        "email": userData['user_email'],
        "exp": expires
    }
    # refresh payload generate
    refresh_payload: Dict[str, Any] = {
        "id": userData['refresh_token_id'],
        "userId": userData['user_id'],
        "exp": expires
    }
    #generate tokens
    access_token = jwt.encode(access_payload, token_secret_key, algorithm=algorithm)
    refresh_token = jwt.encode(refresh_payload, token_secret_key, algorithm=algorithm)
    #return tokens
    return ReturnToken(
        access_token=access_token,
        refresh_token=refresh_token,
        token_expiration_date=expires
    )
    
    