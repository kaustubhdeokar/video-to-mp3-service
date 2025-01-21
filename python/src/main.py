from database import get_db
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import init_db, get_db
from database import User
from utils import verify_password, create_access_token, get_password_hash
from pydantic import BaseModel
from utils import get_current_user

app = FastAPI()
security = HTTPBasic()
init_db()

class UserCreate(BaseModel):
    username: str
    password: str

@app.get("/")
def base_call():
    return {"msg":"user successfully created"}

@app.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}
    

@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    print(credentials.username+":"+credentials.password)
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return create_access_token(data={"sub": user.username})

@app.get("/users/me", response_model=dict)
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
