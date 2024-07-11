from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db

router = APIRouter()

@router.get("/admin/stats", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_telegram_id(db, telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)
