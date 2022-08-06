from fastapi import APIRouter, status, HTTPException, responses, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from h11 import Data
from ..import models, oauth2, schemas,utlis
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    #prefix= "/users",
    tags=['Authentication1']
)

@router.post("/login1",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = db.query(models.User1).filter(models.User1.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utlis.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create Token
    access_token = oauth2.create_acess_token(data= {'user_id': user.id})
    #return Token
    return {'access_token': access_token, "token_type": "bearer"}




            

    
    



