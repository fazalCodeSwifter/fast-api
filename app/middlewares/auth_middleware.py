from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config.constant import config
from app.config.prisma import db
security = HTTPBearer()

async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Token decode karein
        token = auth.credentials
        payload = jwt.decode(token, config['TOKEN_SECRET'], algorithms=config['ALGORITHM'])
        user_id = payload.get("userId")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # 2. check user if exist in db
    user = await db.db().users.find_unique(where={ 'id': user_id },)
    if user is None:
        raise credentials_exception
    
    if hasattr(user, 'password'):
        del user.password
        del user.tokens
        del user.refreshTokens
        
    return user # user bind in request (req.user)