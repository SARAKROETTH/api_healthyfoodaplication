from fastapi import FastAPI
from config import engine

import routes.users as user_routes

import models.users as user_table

user_table.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router)
# @app.get("/")
# async def root():
#     return " hello word"