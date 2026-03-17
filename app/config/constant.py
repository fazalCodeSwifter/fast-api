import os
config = {
    'NODE_ENV': os.getenv('NODE_ENV', 'development'),
    'TOKEN_SECRET':os.getenv('CLIENT_TOKEN_SECRET', 'token_secret'),
    'ALGORITHM': "HS256",
    'TOKEN_EXPIRATION_TIME': os.getenv('TOKEN_EXPIRATION_TIME', '30')
}
