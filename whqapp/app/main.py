from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import requests
from dotenv import load_dotenv
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

load_dotenv()  # Загрузка переменных из .env файла

DATABASE_URL = os.getenv('DATABASE_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set")

print(f"DATABASE_URL: {DATABASE_URL}")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
GAME_URL = 'https://whiterabbitquest.online'
CHANNEL_URL = 'https://t.me/redlinerussia'

@app.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_telegram_id(db, telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/check-subscription/")
def check_subscription(chatId: int):
    response = requests.get(f"{TELEGRAM_API_URL}/getChatMember?chat_id=@redlinerussia&user_id={chatId}")
    is_member = response.json().get('result', {}).get('status') not in ['left', 'kicked']
    return {"isMember": is_member}

@app.post("/send-message/")
def send_message(chatId: int, text: str, reply_markup: dict = None):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chatId,
        "text": text,
        "reply_markup": reply_markup
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
