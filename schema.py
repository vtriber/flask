from pydantic import BaseModel, ValidationError

from errors import HttpError


class CreateUser(BaseModel):

    username: str
    password: str
    email: str




def validate_create_user(json_data):
    try:
        user_schema = CreateUser(**json_data)
        return user_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())


class CreateBulletin:

    header: str
    deskription: str
    username: str
    password: str


def validate_create_bulletin(json_data):
    try:
        bulletin_schema = CreateBulletin(**json_data)
        return bulletin_schema.dict()
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())

