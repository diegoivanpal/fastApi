from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list =   [User(id=1, name="Brais", surname="Moure", url="http://123", age =35),
                User(id=2, name="Moure", surname="Dev", url="http://344", age =45),
                User(id=3, name="Ivan", surname="Pal", url="http://675", age =43)]

@router.get("/userjson")
async def users():
    return "Hola Users"

@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)    

# Query
@router.get("/user/")
async def user(id: int):
    return search_user(id)

@router.post("/user/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User :
        raise HTTPException(status_code=204, detail="El usuario ya existe")
        # return{"error":"El usuario ya existe"}
    else : 
        users_list.append(user)
        return user

@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return { "error": "No se ha actualizado el usuario" }
    else:
        return(user)

@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] 
            found = True

    if not found:
            return { "error": "No se ha eliminado el usuario" }

            


    


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return{"error":"No se ha encontrado el usuario"} 


    