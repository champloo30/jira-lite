from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, Token
from app.auth import hashed_pass, verify_pass, create_access_token

router = APIRouter(
  prefix="/auth",
  tags=["auth"]
)

@router.post("/register", response_model=Token)
def register(
  user: UserCreate,
  db: Session = Depends(get_db)
):
  existing = db.query(User).filter(User.email == user.email).first()
  if existing:
    raise HTTPException(status_code=400, detail="Email already registered")
  
  new_user = User(
    email=user.email,
    password=hashed_pass(user.password)
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  token = create_access_token({
    "sub": new_user.email,
    "role": new_user.role
  })

  return {"access_token": token}

@router.post("/login", response_model=Token)
def login(
  user: UserCreate,
  db: Session = Depends(get_db)
):
  db_user = db.query(User).filter(User.email == user.email).first()
  if not db_user or not verify_pass(user.password, db_user.password):
    raise HTTPException(status_code=401, detail="Invalid credentials")
  
  token = create_access_token({
    "sub": db_user.email,
    "role": db_user.role
  })

  return {"access_token": token}
