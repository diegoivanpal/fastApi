from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema
from db.client import db_client

router = APIRouter( prefix="/userdb",
                    tags=["userdb"] , 
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}} )



users_list = []


@router.get("/")
async def users():
    return users_list

# Path
@router.get("/{id}")
async def user(id: int):
    return search_user(id)    

# Query
@router.get("/")
async def user(id: int):
    return search_user(id)

@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user_by_email(user.email)) == User :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
        
    else : 
        user_dict = dict(user)
        del user_dict["id"]
        id = db_client.local.users.insert_one(user_dict).inserted_id

        new_user = user_schema(db_client.local.users.find_one({"_id":id}))
        
        return User(**new_user)

@router.put("/")
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

@router.delete("/ {id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] 
            found = True

    if not found:
            return { "error": "No se ha eliminado el usuario" }


def search_user_by_email(email: str):
   
    try:
        user = user_schema(db_client.local.users.find_one({"email": email}))
        return User(**user)
    except:
        return {"error": "No se ha encontrado el usuario"} 


    