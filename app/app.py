from fastapi import FastAPI
from routers import demo, security

app = FastAPI()
app.include_router(demo.router)
app.include_router(security.router)

