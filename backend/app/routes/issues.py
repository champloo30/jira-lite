from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import SessionLocal
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueResponse, IssueUpdate

router = APIRouter(
  prefix="/issues",
  tags=["issues"]
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# get all issues

@router.get("/", response_model=List[IssueResponse])
def get_issues(db: Session = Depends(get_db)):
  return db.query(Issue).all()

# create issue

@router.post("/", response_model=IssueResponse, status_code=201)
def create_issue(
  issue: IssueCreate,
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

# get issue by id

@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue(
  issue_id: int,
  db: Session = Depends(get_db)
):
  issue = db.query(Issue).filter(Issue.id == issue_id).first()

  if not issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  return issue

# update issue

@router.put("/{issue_id}", response_model=IssueResponse)
def update_issue(
  issue_id: int,
  issue_update: IssueUpdate,
  db: Session = Depends(get_db)
):
  issue = db.query(Issue).filter(Issue.id == issue_id).first()

  if not issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  for field, value in issue_update.dict(exclude_unset=True).items():
    setattr(issue, field, value)

  db.commit()
  db.refresh(issue)
  return issue

# delete issue

@router.delete("/{issue_id}", status_code=204)
def delete_issue(
  issue_id: int,
  db: Session = Depends(get_db)
):
  issue = db.query(Issue).filter(Issue.id == issue_id).first()

  if not issue:
    raise HTTPException(status_code=404, detail="Issue not found")
  
  db.delete(issue)
  db.commit()

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
