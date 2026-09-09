from pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str
user1 = User(id=1, name="John Doe")
print(user1.id)#Returns 1
print(user1.name)#Returns "John Doe"
user2 = User(id=2)#ValidationError