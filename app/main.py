from fastapi import FastAPI   
from . import models  
from .database import engine 
from .router import posts, user 

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(user.router)

@app.get("/")
async def root(): 
    return {"message" : "Hello World !"}

    