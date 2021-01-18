from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from starlette import status

from configs import Authentication
from helpers.security_helpers import get_random_token
from server.endpoints.auth_common import get_current_user_external, create_access_token, \
    authenticate_user, UserExternal, user_can_edit_all
from server.endpoints.auth_common import hash_password
from server.endpoints.auth_data_models import CurrentUserPasswordChangeInput, NewUserInput, Token, UserInternal, \
    UserAuthenticationInternal, UserPermissions, GUEST_USERNAME

router = APIRouter()


@router.post('/token', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
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
def get_current_user_info(current_user: UserExternal = Depends(get_current_user_external)):
    return current_user


@router.put('/current_user/password')
def set_current_user_password(password_change: CurrentUserPasswordChangeInput,
                                    current_user: UserExternal = Depends(get_current_user_external)):
    is_old_password_correct = authenticate_user(current_user.username, password_change.old_password) is not False
    if not is_old_password_correct:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Old password not correct')

    auth_config = Authentication.load()
    user_auth = auth_config.users[current_user.username].authentication
    user_auth.hashed_password = hash_password(password_change.new_password)
    auth_config.save_file()


@router.get('/users')
def get_all_users(can_edit_all=Depends(user_can_edit_all)):
    users = Authentication.load().users
    users_external = [UserExternal(username=username, permissions=user_data.permissions)
                      for username, user_data in users.items()]
    return users_external


@router.post('/users/{username}')
def add_user(username: str, new_user_data: NewUserInput, can_edit_all=Depends(user_can_edit_all)):
    auth_config = Authentication.load()
    if username in auth_config.users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    hashed_password = hash_password(new_user_data.password)
    user_auth = UserAuthenticationInternal(hashed_password=hashed_password)
    new_user_internal = UserInternal(permissions=new_user_data.permissions, authentication=user_auth)

    auth_config.users[username] = new_user_internal
    auth_config.save_file()


@router.put('/users/{username}')
def modify_user(username: str, user_data: NewUserInput, can_edit_all=Depends(user_can_edit_all)):
    if user_data.password:
        delete_user(username, can_edit_all)
        add_user(username, user_data, can_edit_all)
    else:
        auth_config = Authentication.load()
        auth_config.users[username].permissions = user_data.permissions
        auth_config.save_file()


@router.delete('/users/{username}')
def delete_user(username: str, can_edit_all=Depends(user_can_edit_all)):
    auth_config = Authentication.load()
    del auth_config.users[username]
    auth_config.save_file()


def init_authentication():
    users = Authentication.load()
    if users.jwt_secret:
        return

    users.jwt_secret = get_random_token()
    users.save_file()

    first_user = 'admin'
    first_password = get_random_token(length=10)
    admin_permissions = UserPermissions(view_analysis=True, edit_contributors=True, edit_all=True)
    add_user(first_user, NewUserInput(password=first_password, permissions=admin_permissions))

    guest_permissions = UserPermissions(view_analysis=False, edit_contributors=False, edit_all=False)
    add_user(GUEST_USERNAME, NewUserInput(password='dummy', permissions=guest_permissions))

    logger.info(f'\n{"#" * 80}\n\nFIRST TIME CREDENTIALS\n\n  username: {first_user}\n  '
                f'password: {first_password}\n\n'
                f'This will not be shown again unless you delete the file data/config/users.json.\n\n{"#" * 80}')
