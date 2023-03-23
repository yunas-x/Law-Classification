from sqlalchemy.orm import Session
from DBManagement.Incomming.incoming_pydantic_model import document_model_create as model
from DBManagement.Incomming.incoming_entity_model import document_entity as entity


def addIncoming(db: Session, 
                item: model
               ):
    
    """Add incoming entity (entity for doc)

    Returns:
        _type_: db entity that sent to db
    """
    
    db_item = entity(name=item.name, date=item.recieved_on)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
    
def getIncomingByName(db: Session, 
                name: str = None):
    
    """Finds doc with given name
    
    Returns:
        entity if name passed, otherwise False
        might return None
    """
    
    if name != None:
        return db \
        .query(entity) \
        .filter(entity.name == name) \
        .first()
    
    else:
        return False
    
def getIncomingById(db: Session, 
                    id: int = None):
    
    """Finds doc with given id
    
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