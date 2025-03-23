from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schema, database, model, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote', tags = ['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session=Depends(database.get_db)):
    
    user_exist = db.query(model.User).filter(model.User.id == vote.user_id).first()

    post_exist = db.query(model.Post).filter(model.Post.id == vote.post_id).first()

    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with {vote.post_id} not found')

    if not user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with {vote.user_id} not found')
    
    else:
        vote_query = db.query(model.Vote).filter(model.Vote.post_id == vote.post_id, 
                                                 model.Vote.user_id == vote.user_id)
        found_vote = vote_query.first()
        if vote.dir == 1:
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f'User {vote.user_id} has already voted in {vote.post_id}')
            new_vote = model.Vote(post_id = vote.post_id, user_id = vote.user_id)
            db.add(new_vote)
            db.commit()
            return {'message' : 'successfully added vote'}
        else:
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')
            
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {'message' : 'successfully removed vote'}
            


