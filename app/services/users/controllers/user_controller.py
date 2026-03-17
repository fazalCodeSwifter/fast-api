from fastapi import Depends
from app.config.prisma import db, PrismaConnection
from typing import Any
from ..repository.user_repository import UserRepository
from ..repository.tokens_repository import TokenRepository
from ..service.user_service import UserService

# initialte db instance and pass user repository 
def get_db_connection():
    return db

# depandency inject in UserRepository 
def get_user_repositroy(db: PrismaConnection = Depends(get_db_connection)) -> Any:
    return UserRepository(db)

def get_tokens_repositroy(db: PrismaConnection = Depends(get_db_connection)) -> Any:
    return TokenRepository(db)

# depandency inject in UserService 
def get_user_service(
    repo: UserRepository = Depends(get_user_repositroy),
    tokens: TokenRepository = Depends(get_tokens_repositroy)
    ):
    return UserService(repo, tokens)