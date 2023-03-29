from pydantic import BaseModel

class text_model(BaseModel):
    id: int
    text: str
    
    class Config:
        orm_mode = True