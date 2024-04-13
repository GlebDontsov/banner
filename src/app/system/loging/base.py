import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))  # type: ignore
ADMIN_NAME = os.getenv('ADMIN_NAME')
ADMIN_HASHED_PASSWORD = os.getenv('ADMIN_HASHED_PASSWORD')
USER_NAME = os.getenv('USER_NAME')
USER_HASHED_PASSWORD = os.getenv('USER_HASHED_PASSWORD')

fake_users_db = {
    'user': {
        'username': USER_NAME,
        'hashed_password': USER_HASHED_PASSWORD,
    },
    'admin': {
        'username': ADMIN_NAME,
        'hashed_password': ADMIN_HASHED_PASSWORD,
    },
}

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
