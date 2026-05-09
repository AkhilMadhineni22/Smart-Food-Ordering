from sqlalchemy import Column, Integer, Float, String
from app.DB.dbConnection import Base

class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True , index=True)
    name = Column(String, nullable=False)
    skills = Column(String, nullable=False)
    experience = Column(Float, nullable=False)

    current_tickets = Column(Integer, default=0)


