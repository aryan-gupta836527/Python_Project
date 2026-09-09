from pydantic import BaseModel,Field
from datetime import date as Date
class CreateExpense(BaseModel):
    id:int=Field(gt=0)
    title:str=Field(min_length=1)
    amount:int=Field(gt=0)
    category:str=Field(min_length=1)
    date:Date
class PatchExpense(BaseModel):
    id:int=Field(gt=0)
    title:str|None=None
    amount:int|None=Field(default=None,gt=0)
    category:str|None=None
    date:Date|None=None
class PutExpense(BaseModel):
    id:int=Field(gt=0)
    title:str=Field(min_length=1)
    amount:int=Field(gt=0)
    category:str=Field(min_length=1)
    date:Date