from fastapi import FastAPI
from lib.db.init import init

init()
app = FastAPI()
