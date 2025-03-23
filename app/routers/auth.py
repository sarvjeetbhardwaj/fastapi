from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database, schema, model, utils, oauth2


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schema.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()
    print(user.email)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    ## CREATE A TOKEN
    ## RETURN TOKEN

    access_token = oauth2.create_access_token(data = {'user_id': user.id})

    return {'token': access_token, 'token_type': 'bearer'}