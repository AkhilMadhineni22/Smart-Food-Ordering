from app.DB.agent_repository import create_agent
from app.DB.dbConnection import sessionLocal

db = sessionLocal()

create_agent(db, "Rahul", "payment refund billing transaction failure", 5)
create_agent(db, "Anita", "delivery delay rider issue late order tracking", 4)
create_agent(db, "Vikram", "app crash login issue bug technical problem", 5)
create_agent(db, "Sana", "restaurant complaint food quality missing item", 4)

db.close()
