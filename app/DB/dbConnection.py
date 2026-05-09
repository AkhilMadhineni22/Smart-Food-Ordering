from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# database config

DATABASE_UR = 'postgresql://neondb_owner:npg_S3EBizb4wKUn@ep-cold-hill-an86agrx-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# CREATING ENGINE

engine = create_engine(
    DATABASE_UR,
    echo=True
)

sessionLocal = sessionmaker(
    autoflush=False,
    bind= engine
)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

        
