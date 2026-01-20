from fastapi import FastAPI
from config import engine

import routes.users as user_routes

import models.users as user_table
import models.user_role as role_table
import models.user_otp as otp_table

otp_table.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(user_routes.router)
# @app.get("/")
# async def root():
#     return " hello word"