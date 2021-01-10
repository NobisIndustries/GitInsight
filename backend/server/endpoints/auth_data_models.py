from pydantic.main import BaseModel

GUEST_USERNAME = '__GUEST__'


class UserPermissions(BaseModel):
    view_analysis: bool = True
    edit_contributors: bool = False
    edit_all: bool = False


class UserAuthenticationInternal(BaseModel):
    hashed_password: str


class UserInternal(BaseModel):
    permissions: UserPermissions
    authentication: UserAuthenticationInternal


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
