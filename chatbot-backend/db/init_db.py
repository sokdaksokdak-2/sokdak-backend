# db/init_db.py
from db.session import engine
from models.user import User
from db.base import Base

def init_db():
    Base.metadata.create_all(bind=engine)
