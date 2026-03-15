from base_repository import UserBaseRepository
from ....config.prisma import PrismaConnection
from ..schema.user_schema import BaseUser, User
from prisma.types import UsersCreateInput

class UserRepository(UserBaseRepository):
    def __init__(self, db_client: PrismaConnection) -> None:
        self.db = db_client.db()
        
    async def create_user(self, data: BaseUser) -> User:
        try:
            user_input = UsersCreateInput(**data.model_dump())
            created_user = await self.db.users.create(data=user_input)
            if not created_user:
                raise Exception('User create failed')
            return User(**created_user.model_dump())
        except Exception as error:
            raise Exception(error)