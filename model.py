from pydantic import BaseModel,Field,ValidationError
class User(BaseModel):
    id: int=Field(gt=0)
    name: str=Field(min_length=1, max_length=100)
try:
    user1 = User(id=1, name="John Doe")
    print(user1.id)#Returns 1
    print(user1.name)#Returns "John Doe"
    user2 = User(id=-1, name="")#ValidationError
except ValidationError as e:
    print(e)