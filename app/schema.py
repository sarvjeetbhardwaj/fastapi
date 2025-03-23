from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

'''
This file creates pydantic models for sending post data
'''


class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True
    owner_id : int

class PostCreate(PostBase):
    pass

class UserCreateResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id : int
    #title : str INHERITED FROM POSTBASE
    #content : str
    #published : bool
    created_at : datetime
    owner_id : int
    owner : UserCreateResponse

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post : PostResponse
    votes : int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str


class Userlogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir : int
    user_id : int

    
