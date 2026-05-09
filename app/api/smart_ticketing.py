"""
API endpoints for smart ticket resolving
"""

from fastapi import APIRouter, Depends
from app.config import get_settings
from app.services.ticketing_service import TicketService
from app.DB.dbConnection import get_db
from app.models.schemas import SmartTicketingRequest, SmartTicketResponse
import os

router = APIRouter(prefix="/support", tags=[])


ticket_service = TicketService()

@router.post('/smart-ticketing', response_model= SmartTicketResponse )
async def assign_ticket(
    request: SmartTicketingRequest,
    db = Depends(get_db)
):
    return ticket_service.assign_ticket(request.issue_text,db)