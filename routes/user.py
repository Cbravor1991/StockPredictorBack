from fastapi import APIRouter, Response, status
from config.db import connection
from models.user import users
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT
from cryptography.fernet import Fernet

#inicializo fernet para encriptar la contraseña
key = Fernet.generate_key()
cripto = Fernet(key)

user = APIRouter()

@user.get("/users", response_model = list[User], tags = ["users"])
def get_users():
    return connection.execute(users.select()).fetchall()

@user.post("/users", response_model = User, tags = ["users"])
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = cripto.encrypt(user.password.encode("utf-8"))
    result = connection.execute(users.insert().values(new_user))
    print(result.lastrowid)
    return connection.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get("/user/{id}", response_model = User,tags = ["users"])
def get_user(id:str):
    return connection.execute(users.select().where(users.c.id==id)).first()

@user.delete("/user/{id}", status_code = status.HTTP_204_NO_CONTENT, tags = ["users"] )
def delete_user(id:str, user: User):
    connection.execute(users.update().values(name = user.name, 
                                             email =user.email,
                                             password= user.password).where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put("/user/{id}", response_model= User, tags = ["users"])
def update_user(id:str, user: User):
    connection.execute(users.update().values(name = user.name, 
                                             email =user.email,
                                             password= cripto.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    return connection.execute(users.select().where(users.c.id==id)).first()