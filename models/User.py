from pydantic import BaseModel

class User(BaseModel):
    id: int
    name : str
    refresh_token = str