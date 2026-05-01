from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import ssl
import tempfile

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Fix mysql:// to mysql+pymysql:// so SQLAlchemy understands it
if DATABASE_URL and DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# SSL setup - handles both local (ca.pem file) and Render (env variable)
ssl_args = {}

ca_cert_content = os.getenv("CA_CERT_CONTENT")  # on Render
ca_cert_path = os.getenv("CA_CERT_PATH", "ca.pem")  # local

if ca_cert_content:
    # Render: write cert from env variable to a temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
    tmp.write(ca_cert_content.encode())
    tmp.close()
    ssl_context = ssl.create_default_context(cafile=tmp.name)
    ssl_context.check_hostname = False
    ssl_args = {"ssl": ssl_context}
elif os.path.exists(ca_cert_path):
    # Local: read ca.pem directly from backend folder
    ssl_context = ssl.create_default_context(cafile=ca_cert_path)
    ssl_context.check_hostname = False
    ssl_args = {"ssl": ssl_context}

engine = create_engine(
    DATABASE_URL,
    connect_args=ssl_args,
    pool_pre_ping=True  # auto-reconnect if connection drops
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()