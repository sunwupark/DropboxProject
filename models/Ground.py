from models import User
from pydantic import BaseModel

class Ground(BaseModel):
    id : int
    title :str
    maker : User
    photos = str
    expires_in = str
    coordinate = str
    current_people =list[maker]