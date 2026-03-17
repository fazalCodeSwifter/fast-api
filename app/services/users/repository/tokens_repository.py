from typing import Any, Dict
from app.config.constant import config
from datetime import datetime, timedelta, timezone
from .base_repository import TokenBaseRepsitory
from app.config.prisma import PrismaConnection
from typing import Dict, Any
# from ..schema.user_schema import User
from prisma.models import Tokens, RefreshTokens
from app.exception.validation_error import AppValidationError

class TokenRepository(TokenBaseRepsitory):
    def __init__(self, db_client: PrismaConnection) -> None:
        self.db = db_client.db()
        
        # create tokens repository
    async def create_tokens(self, tokens: Dict[str, Any]) -> Dict[str, Any]:
        try:
            days_to_add = int(config['TOKEN_EXPIRATION_TIME'])
            expires = datetime.now(timezone.utc) + timedelta(days=days_to_add)
            # need user id 
            create_access_token: Tokens = await self.db.tokens.create(data={ 'userId': tokens['user_id'], 'revokedAt': None, 'expireAt': expires })
            create_refresh_token: RefreshTokens = await self.db.refreshtokens.create(data={ 'accessTokenId': create_access_token.id, 'userId': tokens['user_id'], 'revokedAt': None, 'expireAt': expires })

            return { 'access_token_id': create_access_token.id, 'refresh_token_id': create_refresh_token.id }
        except Exception as error:
            raise AppValidationError(message=str(error))
 