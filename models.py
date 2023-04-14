from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Connect to the database
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()


# Define the members table
class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    display_name = Column(String)
    nick = Column(String)
    updated_at = Column(DateTime)

    def __init__(self, id, name, last_seen):
        self.id = id
        self.name = name
        self.last_seen = last_seen


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
