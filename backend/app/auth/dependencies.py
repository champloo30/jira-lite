from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth import ALGORITHM, SECRET_KEY
from app.dependencies import get_db
from app.models import Issue, Comment

oauth2_sceme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_sceme)):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid token")
  
# require issue owner or admin
  
def require_issue_owner(
  issue_id: int,
  user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  issue = db.query(Issue).filter(Issue.id == issue_id).first()
  if not issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  if user["role"] != "admin" and issue.created_by != user["sub"]:
    raise HTTPException(status_code=403, detail="Forbidden")
  
  return issue

# require comment owner or admin

def require_comment_owner(
  comment_id: int,
  user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  comment = db.query(Comment).filter(Comment.id == comment_id).first()

  if not comment:
    raise HTTPException(status_code=404, detail="Comment not found")
  
  if user["role"] != "admin" and comment.user_id != user["sub"]:
    raise HTTPException(status_code=403, detail="Forbidden")
  
  return comment

# require issue assignee or admin

def require_issue_assignee(
  issue_id: int,
  user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  issue = db.query(Issue).filter(Issue.id == issue_id).first()

  if not issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  if (user["role"] != "admin" and issue.assigned_to != user["sub"]):
    raise HTTPException(status_code=403, detail="Forbidden")
  
  return issue
