from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import users
from config.db import connection
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str):
    user = connection.execute(users.select().where(users.c.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user