from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from DBManagement.DBContext import Base

from DBManagement.Classified.classified_entity_model import *

class classifier_entity(Base):
    __tablename__ = "Document_Classifier"
    
    class_id = Column(String, primary_key=True, index=True)
    class_type = Column(String, index=True)
    
    classified = relationship("classified_entity", back_populates="type")