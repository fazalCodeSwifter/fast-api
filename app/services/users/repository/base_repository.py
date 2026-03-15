from abc import ABC, abstractmethod
from typing import List
from ..schema.user_schema import User, BaseUser

class UserBaseRepository(ABC):
    @abstractmethod
    async def create_user(self, data: BaseUser) -> User:
        pass
    
    @abstractmethod
    async def update_user(self, data: BaseUser) -> User:
        pass
    
    @abstractmethod
    async def get_all_user(self) -> List[User]:
        pass
    
    @abstractmethod
    async def get_single_user(self, id: str) -> User:
        pass
    