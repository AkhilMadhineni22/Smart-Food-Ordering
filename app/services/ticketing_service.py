"""
Service layer for Smart Ticket Assigning
"""
from app.models.ml_models import TicketAssignmentModel
from app.DB.agent_repository import get_all_agents, update_ticket_count


class TicketService:
    def __init__(self):
        self.model = TicketAssignmentModel()

    def assign_ticket(self, issue_text: str, db):
        agents = get_all_agents(db)
        if not agents:
            return{
                "error":"no agents available"
            }
        agents_list = [
            {
                "id": a.id,
                "name": a.name,
                "skills": a.skills,
                "experience": a.experience,
                "current_tickets": a.current_tickets
            }
            for a in agents
        ]

        self.model.agents = agents_list

        result =self.model.assign(issue_text)

        update_ticket_count (db,result["agent_id"])

        return result
    
    