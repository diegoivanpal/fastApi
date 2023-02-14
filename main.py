from fastapi import FastAPI
from routers import products, user, basic_auth_users, jwt_auth_users, user_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(products.router)
app.include_router(user.router)

app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(user_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}