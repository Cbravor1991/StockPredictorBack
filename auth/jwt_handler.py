from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKE_EXPIRE_MINUTES
from schemas.token import TokenData

def create_access_token(data:dict, expires_delta: Union[timedelta, None] =None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKE_EXPIRE_MINUTES)   
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encode_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data
            
 

        