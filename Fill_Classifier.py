from DAO.classifier_dao import addClassification
from DBManagement.Classifier.classifier_pydantic_model import classifier_model as model
from DBManagement.DBContext import SessionLocal

def fill_classifier(filename: str):
    """This script is used to fill the classifier table
        Requires SessionLocal defined: sessionmaker which yields Session
        Requires pydantic model and addClassification method
        Data should be provided in {<id>. <name>} file
        There's only one type for one line
        
        e.g. 01.01.01. Constitution
        
        01.02.03 Civil Law -> is incorrect
        0.20.301 Crimes. 023.02.03 Cities -> is incorrect

    Args:
        filename (str): a path where your classifier lies
    """
    
    with open(filename, encoding="utf-8", errors="replace") as file:
        lines = file.readlines()

        for line in lines:
            a, b = line.split('. ', 1)
            a += '.'
            
            print(a, b)
            
            try:
                addClassification(SessionLocal(), model(class_id=a, class_type=b))
                print("Added")
            except:
                print("Error. Key exists or connection malfunctions")
                
    

filename = r"C:\Users\yunas\OneDrive\Рабочий стол\CourseWork\DBManagement\Classes.txt"
# Убрать хардкод при обновлении
"""Path to file where classifier is"""

if __name__ == "__main__":
    fill_classifier(filename=filename)

            
            
            
    
    