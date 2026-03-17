from fastapi import APIRouter
from app.services.users.routes import router as user_router


api_router = APIRouter(prefix='/auth')

api_router.include_router(user_router)