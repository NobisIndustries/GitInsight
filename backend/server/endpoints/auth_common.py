from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from configs import Authentication
from helpers.security_helpers import get_random_token
from server.endpoints.auth_data_models import GUEST_USERNAME, UserExternal

auth_data = Authentication.load()
JWT_SECRET_KEY = auth_data.jwt_secret
JWT_EXPIRE_MINUTES = auth_data.jwt_expires_in_min
JWT_ALGORITHM = 'HS256'
del auth_data


pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/token')


def hash_password(password, salt):
    return pwd_context.hash(f'{salt}{password}')


def __verify_password(password, user_data_internal):
    hashed_password = hash_password(password, user_data_internal.authentication.salt)
    return hashed_password == user_data_internal.authentication.hashed_password


def __get_user_data_internal(username):
    users = Authentication.load().users
    return users.get(username, None)


def authenticate_user(username: str, password: str) -> UserExternal:
    user_data_internal = __get_user_data_internal(username)
    if user_data_internal is None:
        return False
    if __verify_password(password, user_data_internal) or username == GUEST_USERNAME:
        return UserExternal(username=username, permissions=user_data_internal.permissions)
    return False


def create_access_token(data: dict):
    timedelta(minutes=JWT_EXPIRE_MINUTES)
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


async def get_current_user_external(token: str = Depends(oauth2_scheme)) -> UserExternal:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_data_internal = __get_user_data_internal(username)
    if user_data_internal is None:
        raise credentials_exception
    return UserExternal(username=username, permissions=user_data_internal.permissions)


def user_can_view_analysis(current_user: UserExternal = Depends(get_current_user_external)):
    if not current_user.permissions.view_analysis:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Missing permission to view analysis')
    return True


def user_can_edit_contributors(current_user: UserExternal = Depends(get_current_user_external)):
    if not current_user.permissions.edit_contributors:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Missing permission to edit contributors')
    return True


def user_can_edit_all(current_user: UserExternal = Depends(get_current_user_external)):
    if not current_user.permissions.edit_all:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Missing permission to edit all')
    return True


def init_authentication():
    users = Authentication.load()
    if not users.jwt_secret:
        users.jwt_secret = get_random_token()
        users.save_file()
