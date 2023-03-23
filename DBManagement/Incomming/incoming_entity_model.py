from sqlalchemy.orm import relationship
from sqlalchemy import Column, Date, Integer, String
from DBManagement.DBContext import Base

from DBManagement.Classified.classified_entity_model import *

class document_entity(Base):

    __tablename__ = "Document"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    
    classified = relationship('classified_entity', back_populates="document")