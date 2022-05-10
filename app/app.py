from fastapi import FastAPI
from routers import demo, security
from repositories.database import Database

app = FastAPI()
app.include_router(demo.router)
app.include_router(security.router)

Database.initialize('my-db-name')

