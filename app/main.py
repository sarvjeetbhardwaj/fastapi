from fastapi import FastAPI
from . import model
from .database import engine
from . import model
from .routers import post, user, vote #auth,
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

model.BASE.metadata.create_all(bind=engine) #This creates the tables in the database, if alembic is not being used

origins = ['*']
    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#my_posts = [{'title':'title of post1',"content":"content of post 2", "id":1},
#            {'title':'title of post2',"content":"content of post 2", "id":2}]

app.include_router(post.router)
app.include_router(user.router)
#app.include_router(auth.router)
app.include_router(vote.router)



'''

@app.get('/sqlalchemy')
def test_posts(db:Session= Depends(get_db)):
    posts = db.query(model.Post).all()
    return {'data' : posts}


@app.get('/')
async def root():
    return {'message':'Hello world'}

@app.get('/posts', response_model=List[schema.PostResponse]) ## List is used to return all the values as list else it will give error
def get_posts(db:Session= Depends(get_db)):
    #cursor.execute('Select * from posts')
    #posts = cursor.fetchall()
    posts = db.query(model.Post).all()
    print(posts)

    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(new_post:schema.PostCreate, db:Session= Depends(get_db)):
    #cursor.execute('Insert into posts (title , content, published) values (%s, %s, %s) returning *', 
    #               (new_post.title, new_post.content, new_post.published))
    
    #new_post_created = cursor.fetchone()
    #conn.commit()

    #post_to_be_created = model.Post(title = new_post.title, content = new_post.content, published = new_post.published)
    post_to_be_created = model.Post(**new_post.model_dump()) 
    db.add(post_to_be_created)
    db.commit()
    db.refresh(post_to_be_created) ### similar to commit
    return post_to_be_created


#@app.post('/posts')
#def create_post(new_post:Post):
#    return {'data': my_posts}

#@app.post('/posts')
#def create_post(new_post:Post):
#    print(new_post)
#    post_data = new_post.model_dump() ## model_dump  converts the new_post data to dictionary
#    return {'data': post_data}

@app.get('/posts/latest_post')
def get_post_id():
    post = my_posts[len(my_posts)-1]
    return post


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get('/posts/{id}', response_model=schema.PostResponse)
def get_post(id:int, db:Session= Depends(get_db)):
    #cursor.execute('Select * from posts where id = %s', (str(id)))
    #post = cursor.fetchone()
    
    post = db.query(model.Post).filter(model.Post.id == id).first()
    print(post)
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f'Post with id:{id} not found')
    return post


    #post = find_post(id)
    #if not post:
        #response.status_code = 404
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message' : f'post with {id} not found'}
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                    detail=f'Post with id:{id} not found')
    #return {'post_detail': post}



#@app.post('/create_post')
#def create_post(body:Body()):
#    print(body.title)
#    return {'data':body.title, 'content':body.content}
# title str content str

def find_index_post(id):
    for post in my_posts:
        if post['id'] == id:
            post_index = my_posts[post].index
            return post_index

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session= Depends(get_db)):

    #cursor.execute('Delete from posts where id = %s returning *', (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    deleted_post = db.query(model.Post).filter(model.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', response_model=schema.PostResponse)
def update_post(id:int, post:schema.PostCreate, db:Session= Depends(get_db)):
    #cursor.execute('Update posts set title = %s, content = %s, published = %s where id = %s returning *', 
     #              (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(model.Post).filter(model.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schema.UserCreateResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    ## hash the password , user.password
    hashed_password = utils.hash(password = user.password)
    user.password = hashed_password
    new_user = model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/users/{id}', response_model=schema.UserCreateResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} does not exist')
    
    return user'
    ''
'''
