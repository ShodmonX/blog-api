from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=schemas.PostOut)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db)):
    return db.query(models.Post).all()


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(
    post_id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    update_data = updated_post.model_dump(exclude_unset=True)
    post_query.update(update_data, synchronize_session=False)
    db.commit()

    return post_query.first()

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    db.delete(post)
    db.commit()
    return
