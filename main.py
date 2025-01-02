from fastapi import FastAPI
from lib.db.db import init

init()
app = FastAPI()
