from DBManagement.DBContext import Engine
import DBManagement.Classifier.classifier_entity_model as classifier_entity
import DBManagement.Incomming.incoming_entity_model as document_entity
import DBManagement.Classified.classified_entity_model as classified_entity
import DBManagement.Text.text_entity_model as  text_entity


def try_create_datatables():
    """
    Creates datatables in case they doesn't exist
    """
    
    try:
        classifier_entity.Base.metadata.create_all(bind=Engine)
    except:
        print("classifier_entity Already exists")

        
    try:
        document_entity.Base.metadata.create_all(bind=Engine)
    except:
        print("classified_entity Already exists")
        
    try:
        classified_entity.Base.metadata.create_all(bind=Engine)
    except:
        print("classified_entity Already exists")
        
    try:
        text_entity.Base.metadata.create_all(bind=Engine)
    except:
        print("text entity Already exists")
        

if __name__ == '__main__':
    try_create_datatables()