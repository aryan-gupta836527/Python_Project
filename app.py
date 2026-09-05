from flask import Flask,request,jsonify
app=Flask(__name__)
users = []
@app.route("/users",methods=["GET"])
def get_users():
    return jsonify(users),200
@app.route("/users/<int:id>",methods=["GET"]) #Path parameter to get user by ID
def get_user(id):
    if id in [i["id"] for i in users]:
        return jsonify([i for i in users if i["id"]==id]),200
    return jsonify({"Error":f"User with ID {id} not found"}),404
@app.route("/users",methods=["POST"])
def create_user():
    data=request.json
    if data["id"] in [i["id"] for i in users]:
        return jsonify({"Error":f"User with ID {data['id']} already exists"}),400
    users.append(data)
    return jsonify({"Message":"User created","Data":data}), 201
@app.route("/users/<int:id>",methods=["PUT"])
def update_user(id):
    data=request.json
    for i in users:
        if i["id"]==id:
            try:
                i["name"]=data["name"]
                return jsonify({"Message":"User updated","Data":i}),200
            except KeyError:
                return jsonify({"Error":"Invalid data format"}),400
    return jsonify({"Error":f"User with ID {id} not found"}),404
@app.route("/users/<int:id>",methods=["DELETE"])
def delete_user(id):
    for i in users:
        if i["id"]==id:
            users.remove(i)
            return jsonify({"Message":"User deleted"}),200
    return jsonify({"Error":f"User with ID {id} not found"}),404
app.run(debug=True)