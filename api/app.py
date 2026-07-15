from fastapi import FastAPI
from routers import init_routers

app = FastAPI()

init_routers(app=app)
