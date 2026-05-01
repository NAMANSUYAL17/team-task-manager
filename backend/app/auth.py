# JWT and password utilities - no database needed here
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Secret key to sign JWT tokens - keep this private!
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123changeme")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # token valid for 1 day

# bcrypt context - this is what hashes passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Converts "mypassword" → "$2b$12$randomhash..." stored in DB
    password=password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    # Creates a signed JWT token with expiry time
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    # Decodes and verifies JWT token, raises error if invalid/expired
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])