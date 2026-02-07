from fastapi import Depends, HTTPException

from app.auth import get_current_user

def require_role(required: str):
  def role_checker(user=Depends(get_current_user)):
    if user["role"] != required:
      raise HTTPException(status_code=403, detail="Forbidden")
    return user
  return role_checker