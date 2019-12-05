from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    userType = Column(String)

#----------------------------------------------------------------------
    def __init__(self, name, password, userType):
        self.name = name
        self.password = password
        self.userType = userType
