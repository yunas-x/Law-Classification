from pydantic import BaseModel

class classifier_model(BaseModel):
    class_id: str
    class_type: str
    
    class Config:
        orm_mode = True