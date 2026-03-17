from .base_repository import UserBaseRepository
from app.config.prisma import PrismaConnection
from typing import Dict, Any
from ..schema.user_schema import User, UserInDB
from prisma.types import UsersCreateInput
from app.exception.validation_error import AppValidationError

class UserRepository(UserBaseRepository):
    def __init__(self, db_client: PrismaConnection) -> None:
        self.db = db_client.db()
        
        # create user repository
    async def create_user(self, data: Dict[str, Any]) -> User:
        try:
            user_input = UsersCreateInput(**data)
            created_user = await self.db.users.create(data=user_input)
            if not created_user:
                raise AppValidationError(message='User create failed', status_code=404)
            return User(**created_user.model_dump())
        except Exception as error:
            raise Exception(error)
        
        # find one user 
    async def find_user(self, email: str) -> UserInDB | None:
        try:
            user = await self.db.users.find_unique(where={ 'email': email })
            if user:
                return UserInDB(**user.model_dump())
            else:
                return None
        except Exception as error:
            raise error
        