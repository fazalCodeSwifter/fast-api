from abc import ABC, abstractmethod
from typing import Dict, Any
# from typing import List
from ..schema.user_schema import User, UserInDB

class UserBaseRepository(ABC):
    @abstractmethod
    async def create_user(self, data: Dict[str, Any]) -> User:
        pass
    
    # @abstractmethod
    # async def update_user(self, data: BaseUser) -> User:
    #     pass
    
    # @abstractmethod
    # async def find_all_user(self) -> List[User]:
    #     pass
    
    @abstractmethod
    async def find_user(self, email: str) -> UserInDB | None:
        pass
    
    
class TokenBaseRepsitory(ABC):
    @abstractmethod
    async def create_tokens(self, tokens: Dict[str, Any]) -> Dict[str, Any]:
        pass