from .. import model, schema, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func
#from .. import oauth2

router = APIRouter(
    prefix='/posts', tags=['Posts']
)

@router.get('/', response_model=List[schema.PostOut]) ## List is used to return all the values as list else it will give error
#def get_posts(db:Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
def get_posts(db:Session= Depends(get_db), limit: int = 10, skip: int=0, search:Optional[str]= ''):

    #posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()

    posts = db.query(model.Post, func.count(model.Vote.post_id).label('votes')).\
                                                    join(model.Vote, model.Vote.post_id == model.Post.id,isouter=True)\
                                                    .group_by(model.Post.id)\
                                                    .filter(model.Post.title.contains(search))\
                                                    .limit(limit=limit)\
                                                    .offset(offset=skip).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
#def get_posts(new_post:schema.PostCreate, db:Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
def create_post(new_post:schema.PostCreate, db:Session= Depends(get_db)):
    
    
    post_to_be_created = model.Post(**new_post.model_dump())
    #post_to_be_created = model.Post(owner_id= current_user.id, **new_post.model_dump()) 
    #print(current_user.id)
    db.add(post_to_be_created)
    db.commit()
    db.refresh(post_to_be_created) ### similar to commit
    return post_to_be_created


@router.get('/{id}', response_model=schema.PostOut)
#def get_post(id:int, db:Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
def get_post(id:int, db:Session= Depends(get_db)):

    #post = db.query(model.Post).filter(model.Post.id == id).first()

    posts = db.query(model.Post, func.count(model.Vote.post_id).label('votes')).\
                                                    join(model.Vote, model.Vote.post_id == model.Post.id,isouter=True)\
                                                    .group_by(model.Post.id).filter(model.Post.id == id).first()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f'Post with id:{id} not found')
    return posts

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
#def delete_post(id: int, db:Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
def delete_post(id: int, db:Session= Depends(get_db)):

    deleted_post_query = db.query(model.Post).filter(model.Post.id == id)

    if deleted_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')

    #if deleted_post_query.owner_id != oauth2.current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perfrom requested action')

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schema.PostResponse)
#def update_post(id:int, post:schema.PostCreate, db:Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
def update_post(id:int, post:schema.PostCreate, db:Session= Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')

    #if updated_post.owner_id != oauth2.current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perfrom requested action')

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
