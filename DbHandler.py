
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///./learndocs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

class DbHandler:
    def __init__(self):
        self.db = local_session()

    def get_db(self):
        return self.db

    def close(self):
        self.db.close()
