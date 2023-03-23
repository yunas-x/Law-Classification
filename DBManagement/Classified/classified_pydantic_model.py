from pydantic import BaseModel

class classified_model(BaseModel):
    id: int
    result: str
    
    class Config:
        orm_mode = True