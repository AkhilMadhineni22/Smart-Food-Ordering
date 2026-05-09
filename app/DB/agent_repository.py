from sqlalchemy.orm import Session
from app.DB.model import Agent

def create_agent(db: Session, name: str, skills: str, experience: float):
    agent = Agent(
        name = name,
        skills = skills,
        experience = experience,
        current_tickets = 0
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent
# get all agents
def get_all_agents(db:Session):
    return db.query(Agent).all()

#get agent by ID
def get_agent_by_id(db:Session, agent_id: int):
    return db.query(Agent).filter(Agent.id == agent_id).first()

# UPDATE TICKET COUNT

def update_ticket_count(db: Session, agent_id: int, increment: int = 1):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()


    if agent:
        agent.current_tickets += increment
        db.commit()
        db.refresh(agent)

    return agent

# RESET TICKETS (OPTIONAL)

def reset_all_tickets(db: Session):
    agents = db.query(Agent).all()

    for agent in agents:
        agent.current_tickets = 0

    db.commit()

    return agents

