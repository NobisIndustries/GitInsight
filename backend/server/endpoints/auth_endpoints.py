from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from configs import Authentication
from helpers.security_helpers import get_random_token
from server.endpoints.auth_common import get_current_user_external, create_access_token, \
    authenticate_user, UserExternal, user_can_edit_all
from server.endpoints.auth_common import hash_password
from server.endpoints.auth_data_models import CurrentUserPasswordChangeInput, NewUserInput, Token, UserInternal, \
    UserAuthenticationInternal

router = APIRouter()


@router.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token({'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/current_user', response_model=UserExternal)
async def get_current_user_info(current_user: UserExternal = Depends(get_current_user_external)):
    return current_user


@router.put('/current_user/password')
async def set_current_user_password(password_change: CurrentUserPasswordChangeInput,
                                    current_user: UserExternal = Depends(get_current_user_external)):
    is_old_password_correct = authenticate_user(current_user.username, password_change.old_password) is not False
    if not is_old_password_correct:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Old password not correct')

    auth_config = Authentication.load()
    user_auth = auth_config.users[current_user.username].authentication
    new_salt = get_random_token(length=16)
    user_auth.salt = new_salt
    user_auth.hashed_password = hash_password(password_change.new_password, new_salt)
    auth_config.save_file()


@router.get('/users')
async def get_all_users(can_edit_all=Depends(user_can_edit_all)):
    users = Authentication.load().users
    users_external = [UserExternal(username=username, permissions=user_data.permissions)
                      for username, user_data in users.items()]
    return users_external


@router.post('/users/{username}')
async def add_user(username: str, new_user_data: NewUserInput, can_edit_all=Depends(user_can_edit_all)):
    auth_config = Authentication.load()
    if username in auth_config.users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    new_salt = get_random_token(length=16)
    hashed_password = hash_password(new_user_data.password, new_salt)
    user_auth = UserAuthenticationInternal(hashed_password=hashed_password, salt=new_salt)
    new_user_internal = UserInternal(permissions=new_user_data.permissions, authentication=user_auth)

    auth_config.users[username] = new_user_internal
    auth_config.save_file()


@router.put('/users/{username}')
async def modify_user(username: str, user_data: NewUserInput, can_edit_all=Depends(user_can_edit_all)):
    if user_data.password:
        await delete_user(username, can_edit_all)
        await add_user(username, user_data, can_edit_all)
    else:
        auth_config = Authentication.load()
        auth_config.users[username].permissions = user_data.permissions
        auth_config.save_file()


@router.delete('/users/{username}')
async def delete_user(username: str, can_edit_all=Depends(user_can_edit_all)):
    auth_config = Authentication.load()
    del auth_config.users[username]
    auth_config.save_file()
