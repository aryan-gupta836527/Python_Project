from flask import Flask,request,jsonify
from pydantic import ValidationError
from model import Create_User, Update_User
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY=os.getenv("API_KEY")
def validate_api_key():
    api_key = request.headers.get("X-API-KEY")#To get the API key from the request headers
    if api_key != API_KEY:
        return False
    return True
app=Flask(__name__)
users = []
@app.route("/users",methods=["GET"])
def get_users():
    id = request.args.get("id")
    if id is None:
        return jsonify(users),200
    if not id.isdigit(): 
        return jsonify({"Error":"ID must be an integer"}),400
    id=int(id)
    if id<=0:
        return jsonify({"Error":"ID must be a positive integer"}),400
    for i in users:
        if i["id"]==id:
            return jsonify(i),200
    return jsonify({"Error":f"User with ID {id} not found"}),404
@app.route("/users/<int:id>",methods=["GET"]) #Path parameter to get user by ID
def get_user(id):
    if id in [i["id"] for i in users]:
        return jsonify([i for i in users if i["id"]==id]),200
    return jsonify({"Error":f"User with ID {id} not found"}),404
@app.route("/users",methods=["POST"])
def create_user():
    data=request.get_json(silent=True)#If the client sends invalid JSON, this will return None instead of raising an error
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    try:
        user = Create_User.model_validate(data)
    except ValidationError as e:
        return jsonify({"Error": str(e)}),400
    if user.id in [i["id"] for i in users]:
        return jsonify({"Error":f"User with ID {user.id} already exists"}),400
    user_data=user.model_dump()
    users.append(user_data)
    return jsonify({"Message":"User created","Data":user_data}), 201
@app.route("/users/<int:id>",methods=["PUT"])#We don't need id validation here because we are using path parameter which is already validated by Flask
def update_user(id):
    data=request.get_json(silent=True)
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    try:
        user = Update_User.model_validate(data)
    except ValidationError as e:
        return jsonify({"Error": str(e)}),400
    for i in users:
        if i["id"]==id:
            i["name"]=user.name
            return jsonify({"Message":"User updated","Data":i}),200
    return jsonify({"Error":f"User with ID {id} not found"}),404
@app.route("/users/<int:id>",methods=["DELETE"])
def delete_user(id):
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    for i in users:
        if i["id"]==id:
            users.remove(i)
            return jsonify({"Message":"User deleted"}),200
    return jsonify({"Error":f"User with ID {id} not found"}),404
app.run(debug=True)