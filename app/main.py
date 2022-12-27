from fastapi import FastAPI , Response , status , HTTPException , Depends
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine , get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind = engine)

while True:
    try:
        connection = psycopg2.connect(host="localhost", database = "fastapi", user = "fastapiuser" , password = "fastapiuserpassword", cursor_factory=RealDictCursor )
        cursor = connection.cursor()
        print("DB successfull")
        break
    except:
        print("database error")

app = FastAPI()



class Post(BaseModel):
    title : str
    content : str 
    published : bool = True


my_posts = [{"title": "goa beaches" , "content" : "Top Goa beaches", "id" : 1 },
            {"title": "maharashtra beaches" , "content" : "Top MAH beaches", "id" : 2 }]

@app.get("/")
async def root(): 
    return {"message" : "Hello World !"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db) ):
    posts =  db.query(models.Posts).all()
    print(posts)
    return {"data":posts} 

@app.post("/posts" , status_code= status.HTTP_201_CREATED  )
def create_post(new_post : Post , response : Response , db: Session = Depends(get_db) ):
    #post_dict = new_post.dict()
    cursor.execute("""insert into posts (title,content,published) values (%s , %s , %s ) RETURNING * """ ,
                    (new_post.title, new_post.content,new_post.published))
    new_post_ret = cursor.fetchone() 
    connection.commit()
    return {"message" :  new_post_ret}

@app.get("/posts/{id}")
def get_post(id:int , response :Response , db: Session = Depends(get_db) ):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)  )
    post =cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} was not found")
    return {"data":post}


@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int , response : Response , db: Session = Depends(get_db)):

    cursor.execute(""" DELETE from posts where id = %s  returning * """,(str(id),))
    deleted_post = cursor.fetchone()

    connection.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} was not found")
    return Response(status_code= status.HTTP_204_NO_CONTENT)
    


@app.put("/posts/{id}", status_code=   status.HTTP_202_ACCEPTED )
def update_post(id :int ,new_post : Post ,db: Session = Depends(get_db) ):
    cursor.execute(""" UPDATE posts SET 
    title = %s , content = %s  , published = %s 
    where id = %s  returning * """,(new_post.title,new_post.content,new_post.published ,str(id),))
    connection.commit()
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"{id} was not found for update")  
    return {"updated post " : updated_post }
 
