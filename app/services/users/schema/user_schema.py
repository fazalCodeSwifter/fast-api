from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Annotated
from datetime import datetime, timezone

class BaseUser(BaseModel):
    firstName: Annotated[str, Field(..., min_length=3, max_length=15, description='Enter First name', examples=['Fazal'])]
    lastName: Annotated[Optional[str], Field(min_length=3, max_length=15, description='Enter Last name', examples=['Shah'])]
    username: Annotated[str, Field(..., description='Enter Username', examples=['fazal123'])]
    email: Annotated[EmailStr, Field(..., description='Enter Email', examples=['example@example.com'])]


class CreateUser(BaseUser):
        password: Annotated[str, Field(..., description='Enter password')]

class User(BaseUser):
    id: Annotated[str, Field(...)]
    createdAt: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))]
    updatedAt: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))]
    
    
class UserInDB(User):
    password: Annotated[str, Field(..., description='Enter password')]
    
    
    
class LoginUser(BaseModel):
     email: Annotated[EmailStr, Field(..., description='Enter Email', examples=['example@example.com'])] 
     password: Annotated[str, Field(..., description='Enter password')]