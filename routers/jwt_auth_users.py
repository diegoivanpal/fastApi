from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION= 1
SECRET = "d329e98919526da0551feb767d09e22c2f7c47aec79f70f924d8e273a9a696d4"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
    
users_db = {
    "mouredev" : {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@ourede.com",
        "disabled": False,
        "password": "$2a$12$4ECcLC8y1PNRArghpSpc0.Fo/VqF1Z3XeZNXXH3neaUBtEkT8QlOa"
    },
    "mouredev2" : {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@ourede.com",
        "disabled": True,
        "password": "$2a$12$daJE.WyDTJ6UCTU4psKNCux5WmJzNCXyE5EgdYvxh/XJLpgJwf/T6"
    }

}

def search_user_db(username: str ):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalidas", 
            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        

    except JWTError:
        raise exception

    return search_user(username)
        
    
async def current_user(user: User = Depends(auth_user)): 
    if user.disabled:
        raise HTTPException(
        status_code= status.HTTP_400_BAD_REQUEST, 
        detail="Usuario Inactivo")

    return user




@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    crypt.verify(form.password, user.password)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {
        "sub":user.username,
        "exp":expire,
        
    }

    return {"acces_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

    
@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user