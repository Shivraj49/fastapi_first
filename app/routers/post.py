from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix="/posts1",
    tags=['Posts1']
)


# path Opeartion

@router.get("/", response_model=List[schemas.postOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), Limit: int = 10):
    # models represents tables #all() returns all columns

    al_post = db.query(models.Post1).limit(Limit).all()

    #Join QUERY to get votes
    results = db.query(models.Post1, func.count(models.Vote1.post_id).label("votes")).join(
        models.Vote1, models.Vote1.post_id == models.Post1.id, isouter=True).group_by(models.Post1.id).all()
    return results

    '''cursor.execute("""select * from posts """)
    posts = cursor.fetchall()'''

    # return { 'status': al_post}
    return al_post

# ------------------------------------------------------------------------------------------------


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post_match: schemas.Postcreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post1(owner_id=current_user.id, **
                           post_match.dict())  # unpacked the dictionary
    #new_post= models.Post1(title= post_match.title, content= post_match.content, published= post_match.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Similar as Returning in postgres

    '''cursor.execute(""" insert into posts (title, content, published) values (%s, %s,%s) returning * """,
                   (post_match.title, post_match.content, post_match.published),)
    new_post = cursor.fetchone()
    conn.commit()  # to push data into database'''

    # return {"new _post": new_post}
    return new_post

    # print(post_match.dict())

    # post_dict = post_match.dict()
    # post_dict["id"] = randrange(1, 1000000000)
    # my_posts.append(post_dict)

# ------------------------------------------------------------------------------------------------


@router.get("/{id}", response_model=schemas.postOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # Convert id into int
    '''cursor.execute(""" select * from posts where id = %s""", (str(id),))
    gt_post = cursor.fetchone()'''

    gt_post = db.query(models.Post1).filter(models.Post1.id == id).first()
    
    if not gt_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post1 with id:{id} was not found")
        
    #Join QUERY to get votes
    results = db.query(models.Post1, func.count(models.Vote1.post_id).label("votes")).join(
        models.Vote1, models.Vote1.post_id == models.Post1.id, isouter=True).group_by(models.Post1.id).first()
    
    return results

    # print(id)
    # post = find_post(id)
    

        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"Post1 with {id} was not found"}

    # return {"post details": gt_post}
    return gt_post

# ------------------------------------------------------------------------------------------------


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deleting post
    # find the index int h array that has requird ID

    deleted_post = db.query(models.Post1).filter(models.Post1.id == id).delete()
    db.commit()

    ''' cursor.execute(
        """ delete from posts where id = %s returning *""""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()'''

    #index = find_index_post(id)

    if (deleted_post == None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post1 with id: {id} does not exist")
    # my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------------------------------------------------


@router.put("/{id}")
def update_post_fun(id: int, post_match: schemas.Postupdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    updated_post = db.query(models.Post1).filter(
        models.Post1.id == id).update(post_match.dict())
    db.commit()

    # print(post_match)
    '''cursor.execute("""update posts set title= %s, content= %s, published= %s where id = %s returning *""",
                   (post_match.title, post_match.content, post_match.published, str(id)))
    
    updated_post= cursor.fetchone()
    conn.commit()'''
    #index = find_index_post(id)

    if (updated_post == None):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post1 with id: {id} does not exist")

    # post_dict = post_match.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    # return {'message': updated_post}
    return updated_post
