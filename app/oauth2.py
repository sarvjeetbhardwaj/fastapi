#from jose import JOSEError, jwt, JWTError
from datetime import datetime, timedelta, timezone
from . import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database
from . import model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#secret key
##algorithm
#expiration time
SECRET_KEY = '098DJJHWDIUALXNCbhuyshbsgyhcdhosjsh668uw9wu84578986527376dhsncux'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception  = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                           detail='Could not validate credentials', 
                                           headers={'WWW-Authenticate': 'Bearer'})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(model.User).filter(model.User.id == token.id).first()
    
    return user
