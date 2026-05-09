from app.DB.dbConnection import engine, Base
from app.DB.model import Agent

Base.metadata.create_all(bind=engine)
