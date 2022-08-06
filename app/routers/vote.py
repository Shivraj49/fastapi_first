from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2


router = APIRouter(
    prefix="/vote1",
    tags=['Vote1']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post1).filter(models.Post1.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post1 with id: {vote.post_id} does not exist")

    vote_query = db.query(models.Vote1).filter(models.Vote1.post_id == vote.post_id, models.Vote1.user_id == current_user.id)

    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        new_vote = models.Vote1(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote1 does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}