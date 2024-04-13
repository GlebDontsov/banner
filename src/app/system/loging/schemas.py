from pydantic import BaseModel


class Token(BaseModel):
    """Токен."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Пользователь токена."""

    username: str | None = None


class User(BaseModel):
    """Пользователь в БД, без хешированного пароля."""

    username: str


class UserInDB(User):
    """Пользователь в БД."""

    hashed_password: str
