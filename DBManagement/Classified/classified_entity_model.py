from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from DBManagement.DBContext import Base

from DBManagement.Classifier.classifier_entity_model import *
from DBManagement.Incomming.incoming_entity_model import *

class classified_entity(Base):
    __tablename__ = "Classified"
    
    id = Column(Integer, ForeignKey('Document.id'), primary_key=True, index=True)
    result = Column(String, ForeignKey('Document_Classifier.class_id'), primary_key=True, index=True)
    
    document = relationship('document_entity', back_populates="classified")
    type = relationship('classifier_entity', back_populates="classified")