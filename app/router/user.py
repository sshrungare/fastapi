from .. import models , utils , schemas
from fastapi import   status , HTTPException , Depends , APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user" , tags=["Demo1"]
)

@router.get("/{id}" , response_model= schemas.ResponseCreateUser)
def get_user( id :int, db: Session = Depends(get_db) ):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found" ) 
    
    return user


@router.post("/" , status_code= status.HTTP_201_CREATED , response_model= schemas.ResponseCreateUser )
def create_user( user : schemas.RequestCreateUser ,db: Session = Depends(get_db) ):
    password_hash = utils.hash(user.password)
    user.password = password_hash
    new_user = models.Users(**user.dict())
    try:
        db.add(new_user)
        db.commit()
    except:
        raise "Database Error"
    db.refresh(new_user)
    return new_user


