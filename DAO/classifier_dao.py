from sqlalchemy.orm import Session
from DBManagement.Classifier.classifier_pydantic_model import classifier_model as model
from DBManagement.Classifier.classifier_entity_model import classifier_entity as entity

def addClassification(db: Session, 
                      item: model
                     ):
    
    """Add classification entity (key and value)

    Returns:
        _type_: db entity that sent to db
    """
    
    db_item = entity(class_id=item.class_id, class_type=item.class_type)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
    
def getClassification(db: Session, 
                  id: str = None):
    
    """Finds classifier with given id
    
    Returns:
        entity if id passed, otherwise False
        might return None
    """
    
    if id != None:
        return db \
        .query(entity) \
        .filter(entity.class_id == id) \
        .first()
    
    else:
        return False