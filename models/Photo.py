from pydantic import BaseModel

class Photo(BaseModel):
    id : int
    title :str
    src : str
    thumbnail :str
    uploaded_at :str