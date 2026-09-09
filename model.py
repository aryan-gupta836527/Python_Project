from pydantic import BaseModel,Field,ValidationError
class Create_User(BaseModel):
    id: int=Field(gt=0)
    name: str=Field(min_length=1, max_length=100)
class Update_User(BaseModel):
    name: str=Field(min_length=1, max_length=100)