from pydantic import BaseModel,Field,ValidationError
class User(BaseModel):
    id: int=Field(gt=0)
    name: str=Field(min_length=1, max_length=100)
try:
    user1 = User(id=1, name="John Doe")
    data={"id": 2, "name": "Bob Johnson"}
    user2 = User.model_validate(data)#pydantic model
    print(user1.id)#Returns 1
    print(user1.name)#Returns "John Doe"
    print(user2.id)#Returns 2
    print(user2.name)#Returns "Bob Johnson"
    data2=user2.model_dump()
    print(data2)#dict
    user3 = User(id=-1, name="")#ValidationError
except ValidationError as e:
    print(e)