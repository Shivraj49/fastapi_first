from fastapi import status, HTTPException,Depends,APIRouter
from ..import models, schemas,utlis
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/users1",
    tags=['Users1']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password= utlis.hash(user.password)
    user.password = hashed_password
    new_user= models.User1(**user.dict())  #unpacked the dictionary
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Similar as Returning in postgres
    
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User1).filter(models.User1.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"USER not found")
    
    return user
    