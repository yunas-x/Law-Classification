from sqlalchemy.orm import Session
from DBManagement.Text.text_pydantic_model import text_model as model
from DBManagement.Text.text_entity_model import text_entity as entity

def addText(db: Session, 
                  item: model
                 ):
    
    """Add classified entity (entity for classified doc)

    Returns:
        _type_: db entity that sent to db
    """
    
    db_item = entity(id=item.id, text=item.text)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def getText(db: Session, 
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