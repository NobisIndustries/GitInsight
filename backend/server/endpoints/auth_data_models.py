from pydantic.main import BaseModel


GUEST_USERNAME = '__GUEST__'


class UserPermissions(BaseModel):
    view_analysis: bool = True
    edit_contributors: bool = False
    edit_all: bool = False


class UserAuthenticationInternal(BaseModel):
    hashed_password: str
    salt: str


class UserInternal(BaseModel):
    permissions: UserPermissions
    authentication: UserAuthenticationInternal


def create_default_user():
    # Since at first setup nobody has an account, you can do everything without being logged in. The
    # frontend should prompt the first user to make himself an admin user and limit the guest permissions
    permissions = UserPermissions(view_analysis=True, edit_contributors=True, edit_all=True)
    auth = UserAuthenticationInternal(hashed_password='', salt='')
    return {GUEST_USERNAME: UserInternal(permissions=permissions, authentication=auth)}


# ------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class CurrentUserPasswordChangeInput(BaseModel):
    old_password: str
    new_password: str


class NewUserInput(BaseModel):
    password: str
    permissions: UserPermissions


class UserExternal(BaseModel):
    username: str
    permissions: UserPermissions
