from pydantic import BaseModel , EmailStr 
from datetime import datetime
 

class PostBase(BaseModel):
    title : str
    content : str 
    published : bool = True

class PostCreate(PostBase):
    pass 
 
class PostResponse(BaseModel):
    title : str 
    content : str 
    published : bool 
    created_at : datetime
    class Config:
        orm_mode = True

class RequestCreateUser(BaseModel):
    email: EmailStr 
    password : str 


class ResponseCreateUser(BaseModel):
    id: int
    email: EmailStr 
    class Config:
        orm_mode = True

