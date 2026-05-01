# This file is used by every protected route
# FastAPI calls get_current_user automatically when a route has Depends(get_current_user)
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .auth import decode_token
from .models import User

# Tells FastAPI where the login endpoint is, so /docs shows "Authorize" button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),  # extracts Bearer token from request header
    db: Session = Depends(get_db)         # gets a database session
):
    try:
        payload = decode_token(token)         # decode JWT → get {"sub": "42", "exp": ...}
        user_id = payload.get("sub")          # "sub" holds the user's ID
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user  # this user object is injected into the route function
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")