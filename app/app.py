from fastapi import FastAPI
from routers import demo, security, user_management
from repositories.database import Database

app = FastAPI()
app.include_router(demo.router)
app.include_router(security.router)
app.include_router(user_management.router)

Database.initialize('my-db-name')

