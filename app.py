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
app.run(debug=True)