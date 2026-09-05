from flask import Flask,request,jsonify
from validation import validate_create_user, validate_update_user
app=Flask(__name__)
users = []
@app.route("/users",methods=["GET"])
def get_users():
    id = request.args.get("id")
    if id is None:
        return jsonify(users),200
    if id.isdigit()==False:
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
    validation_error = validate_create_user(data)
    if validation_error:
        return jsonify({"Error": validation_error}),400
    if data["id"] in [i["id"] for i in users]:
        return jsonify({"Error":f"User with ID {data['id']} already exists"}),400
    #line 14-30 are validation checks for incoming data
    users.append(data)
    return jsonify({"Message":"User created","Data":data}), 201
@app.route("/users/<int:id>",methods=["PUT"])#We don't need id validation here because we are using path parameter which is already validated by Flask
def update_user(id):
    data=request.get_json(silent=True)
    validation_error = validate_update_user(data)
    if validation_error:
        return jsonify({"Error": validation_error}),400
    for i in users:
        if i["id"]==id:
            i["name"]=data["name"]
            return jsonify({"Message":"User updated","Data":i}),200
    return jsonify({"Error":f"User with ID {id} not found"}),404
@app.route("/users/<int:id>",methods=["DELETE"])
def delete_user(id):
    for i in users:
        if i["id"]==id:
            users.remove(i)
            return jsonify({"Message":"User deleted"}),200
    return jsonify({"Error":f"User with ID {id} not found"}),404
app.run(debug=True)