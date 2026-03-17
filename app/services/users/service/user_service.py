from ..repository.user_repository import UserRepository
from ..repository.tokens_repository import TokenRepository
from ..schema.user_schema import CreateUser, User, LoginUser
from ..core.security import Security
from app.exception.validation_error import AppValidationError
from app.middlewares.success_response import JsonResponse
from fastapi.responses import JSONResponse
from app.helpers.generate_tokens import generate_token


class UserService:
    def __init__(self, userModel: UserRepository, tokenModel: TokenRepository) -> None:
        self.model = userModel
        self.tokenModel = tokenModel
        # sign up user service
    async def create_user_data(self, data: CreateUser) -> User:
        try:
            # check if existing user
            existing_user = await self.model.find_user(data.email)
            if existing_user:
                raise AppValidationError(message='Email already exist', status_code=400)
            # if not then create new user 
            
            # hashing password
            hashed_password = Security.get_password_hash(data.password)
            user_dict =  data.model_dump()
            user_dict['password'] = hashed_password
            create_new_user = await self.model.create_user(data=user_dict)
            return User(**create_new_user.model_dump(exclude={'password'}))
        except Exception as error:
            raise error
    
    # login user service
    async def login_user(self, data: LoginUser) -> JSONResponse:
        try:
            # find user via email
            exist_user = await self.model.find_user(data.email)
            if not exist_user:
                raise AppValidationError(message='Invalid email or password', status_code=401)
            # if not exist then raise validation error
            is_valid = Security.verify_password(data.password, exist_user.password)
            if not is_valid:
                raise AppValidationError(message='Invalid email or password', status_code=401)
            #if exist user then login 
            # 1. create data for access token and refresh token 
            create_tokens = await self.tokenModel.create_tokens({ 'user_id': exist_user.id })
            
            generate_tokens = await generate_token({ 
                                                        'user_id': exist_user.id,
                                                        'user_email': exist_user.email,
                                                        'access_token_id': create_tokens['access_token_id'],
                                                        'refresh_token_id': create_tokens['refresh_token_id']
                                                    })
            return JsonResponse.success(data=generate_tokens)
        except Exception as error:
            raise error