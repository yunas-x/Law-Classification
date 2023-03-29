from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from DBManagement.DBContext import Base

from DBManagement.Classified.classified_entity_model import *

class text_entity(Base):

    __tablename__ = "Text"
    
    id = Column(Integer, ForeignKey('Document.id'), primary_key=True, index=True)
    text = Column(String)
    
    document = relationship('document_entity', back_populates="text")