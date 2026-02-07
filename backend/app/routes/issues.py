from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db
from app.models import Issue, User
from app.schemas import IssueCreate, IssueResponse, IssueUpdate
from app.auth import get_current_user, require_role, require_issue_owner, require_issue_assignee
from app.utils import VALID_TRANSITIONS

router = APIRouter(
  prefix="/issues",
  tags=["issues"]
)

# get all issues

@router.get("/", response_model=List[IssueResponse])
def get_issues(
  user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  return db.query(Issue).all()

# get issue by id

@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue(
  issue_id: int,
  user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  issue = db.query(Issue).filter(Issue.id == issue_id).first()

  if not issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  return issue

# search issues

@router.get("/", response_model=List[IssueResponse])
def search_issues(
  status: Optional[str] = Query(None),
  search: Optional[str] = Query(None),
  db: Session = Depends(get_db)
):
  query = db.query(Issue)

  if status:
    query = query.filter(Issue.status == status)
  
  if search:
    query = query.filter(Issue.title.ilike(f"%{search}%"))

  return query.all()

# create issue

@router.post("/", response_model=IssueResponse, status_code=201)
def create_issue(
  issue: IssueCreate,
  user = Depends(require_role(["admin", "reporter"])),
  db: Session = Depends(get_db)
):
  new_issue = Issue(
    title=issue.title,
    description=issue.description
  )

  db.add(new_issue)
  db.commit()
  db.refresh(new_issue)

  return new_issue

# update issue

@router.put("/{issue_id}", response_model=IssueResponse)
def update_issue(
  issue_update: IssueUpdate,
  db_issue = Depends(require_issue_owner),
  db: Session = Depends(get_db)
):
  db_issue.title = issue_update.title
  db_issue.description = issue_update.description
  db.commit()
  db.refresh(db_issue)

  return db_issue

# assign issue

@router.put("/{issue_id}/assign/{user_id}")
def assign_issue(
  issue_id: int,
  user_id: int,
  _: dict = Depends(require_role(["admin", "developer"])),
  db: Session = Depends(get_db)
):
  db_issue = db.query(Issue).filter(Issue.id == issue_id).first()

  if not db_issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  user = db.query(User).filter(User.id == user_id).first()

  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  
  db_issue.assigned_to = user_id
  db.commit()
  db.refresh(db_issue)

  return {"message": f"Issue {issue_id} assigned to user {user_id}"}

# update issue status

@router.put("/{issue_id}/status")
def update_status(
  issue_id: int,
  status: str,
  db_issue = Depends(require_issue_assignee),
  db: Session = Depends(get_db)
):
  allowed = VALID_TRANSITIONS.get(db_issue.status, [])

  if status not in allowed:
    raise HTTPException(status_code=400, detail=f"Invalid status transition from {db_issue.status} to {status}")
  
  # auto assign when work begins
  if db_issue.status == "open" and status == "in_progress":
    db_issue.assigned_to = db_issue.assigned_to or db_issue.created_by
  
  db_issue.status = status
  db.commit()
  db.refresh(db_issue)

  return {"message": f"Issue status updated to {status}"}

# delete issue

@router.delete("/{issue_id}", status_code=204)
def delete_issue(
  issue_id: int,
  user = Depends(require_role("admin")),
  db: Session = Depends(get_db)
):
  issue = db.query(Issue).filter(Issue.id == issue_id).first()

  if not issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  db.delete(issue)
  db.commit()
