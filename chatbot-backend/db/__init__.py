from .session import engine
# from models import member, emotion  # import all models here

def init_db():
    Base.metadata.create_all(bind=engine)
