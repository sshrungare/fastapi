from .. import models , schemas
from fastapi import   Response , status , HTTPException , Depends , APIRouter
from ..database import   get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/posts"
)

@router.get("/" , response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db) ):
    posts =  db.query(models.Post).all()
    #print(posts)
    return posts

@router.post("/" , status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse  )
def create_post(new_post : schemas.PostCreate , response : Response , db: Session = Depends(get_db) ):
    n_post = models.Post(**new_post.dict())
    db.add(n_post)
    db.commit()
    db.refresh(n_post)
    return n_post

@router.get("/{id}")
def get_post(id:int , response :Response , db: Session = Depends(get_db) , response_model= schemas.PostResponse  ):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} was not found")
    return post


@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int , response : Response , db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)
    


@router.put("/posts/{id}", status_code=   status.HTTP_202_ACCEPTED , response_model= schemas.PostResponse  )
def update_post(id :int ,new_post : schemas.PostCreate ,db: Session = Depends(get_db) ):
    post_query = db.query(models.Post).filter(models.Post.id == id )
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} was not found")
     
    post_query.update(new_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
 