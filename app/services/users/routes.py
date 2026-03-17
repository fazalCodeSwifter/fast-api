from fastapi import APIRouter, Depends, status, HTTPException
from .schema.user_schema import User, CreateUser, LoginUser
from .service.user_service import UserService
from .controllers.user_controller import get_user_service
from typing import Dict, Any

router = APIRouter(prefix='/user', tags=['Users'])

@router.post('/sign-up', response_model=User,  status_code=status.HTTP_201_CREATED)
async def create_users(
    user_in: CreateUser,
    user_serivces: UserService = Depends(get_user_service)
):
    try:
        return await user_serivces.create_user_data(user_in)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )
        
@router.post('/login', response_model=Dict[str, Any],  status_code=status.HTTP_200_OK)
async def login_user(
    user_in: LoginUser,
    user_serivces: UserService = Depends(get_user_service)
):
    try:
        return await user_serivces.login_user(user_in)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )