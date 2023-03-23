from sqlalchemy.orm import Session
from DBManagement.Classified.classified_pydantic_model import classified_model as model
from DBManagement.Classified.classified_entity_model import classified_entity as entity

def addClassified(db: Session, 
                  item: model
                 ):
    
    """Add classified entity (entity for classified doc)

    Returns:
        _type_: db entity that sent to db
    """
    
    db_item = entity(id=item.id, result=item.result)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
    
def getClassified(db: Session, 
                  id: int = None):
    
    """Finds classified doc with given id
    
    Returns:
        entity if id passed, otherwise False
        might return None
    """
    
    if id != None:
        return db \
        .query(entity) \
        .filter(entity.id == id) \
        .first()
    
    else:
        return False