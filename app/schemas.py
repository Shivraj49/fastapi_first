
from datetime import datetime
from typing import Optional
from pydantic import EmailStr,conint
from pydantic import BaseModel

#Pydantic Model
# title: string,  content: string

#!USER
#Request
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
#Response
class UserOut (BaseModel):
    id : int
    email: str
    created_at : datetime
    
    
    class Config:
        orm_mode = True
        
#!POST
#Post_ Request
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # to Create Optional Field and Default value is True
    
class Postcreate(PostBase): #extends Post Class 
    pass
    
class Postupdate(PostBase):
    pass

#Post_Response
class Post (PostBase):
    id : int
    created_at : datetime
    owner_id: int
    owner: UserOut  #return pydantic model UserOut
    
    class Config:
        orm_mode = True

class postOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
            
#!Authentication
#request
class UserLogin(BaseModel):
    email: EmailStr
    password : str
    
#Response

#!TOKEN
#Response
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    
#!VOTE
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)