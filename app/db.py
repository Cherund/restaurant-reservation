import logging
from sqlmodel import create_engine, Session, SQLModel
from app.config import DATABASE_URL

logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Connected to database and tables created.")

def get_session():
    with Session(engine) as session:
        yield session
