from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str

class UpdateUser(BaseModel):
    name: str = None