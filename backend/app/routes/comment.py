from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Issue, Comment
from app.schemas import CommentCreate, CommentOut
from app.auth import get_current_user, require_comment_owner

router = APIRouter(
  prefix="/issues/{issue_id}/comments",
  tags=["comments"]
)

# list comments

@router.get("/", response_model=list[CommentOut])
def list_comments(
  issue_id: int,
  user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  return (
    db.query(Comment)
    .filter(Comment.issue_id == issue_id)
    .order_by(Comment.created_at)
    .all()
  )

# create comment

@router.post("/", response_model=CommentOut)
def create_comment(
  issue_id: int,
  comment: CommentCreate,
  user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  db_issue = db.query(Issue).filter(Issue.id == issue_id).first()

  if not db_issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  new_comment = Comment(
    content=comment.content,
    issue_id=issue_id,
    user_id=user["sub"]
  )

  db.add(new_comment)
  db.commit()
  db.refresh(new_comment)

  return new_comment

# update comment

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(
  comment_update: CommentCreate,
  db_comment = Depends(require_comment_owner),
  db: Session = Depends(get_db)
):
  db_comment.content = comment_update.content
  db.commit()
  db.refresh(db_comment)

  return db_comment

# delete comment
@router.delete("/{comment.id}", status_code=204)
def delete_comment(
  db_comment = Depends(require_comment_owner),
  db: Session = Depends(get_db)
):
  db.delete(db_comment)
  db.commit()

  return {"message": "Comment deleted successfully"}
