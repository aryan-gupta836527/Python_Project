from flask import Flask,request,jsonify
from pydantic import ValidationError
from expenses_model import CreateExpense,PutExpense,PatchExpense
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY=os.getenv("API_KEY")
def validate_api_key():
    api_key=request.headers.get("X-API-KEY")
    if api_key==API_KEY:
        return True
    return False
app=Flask(__name__)
L=[]
@app.route("/expenses",methods=["GET"])
def get_expenses():
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    copy=L.copy()
    category=request.args.get("category")
    min_amt=request.args.get("min_amount")
    max_amt=request.args.get("max_amount")
    if category:
        copy=[i for i in copy if i["category"]==category]
    if min_amt:
        copy=[i for i in copy if i["amount"]>=int(min_amt)]
    if max_amt:
        copy=[i for i in copy if i["amount"]<=int(max_amt)]
    return jsonify(copy),200
@app.route("/expenses/<int:id>",methods=["GET"])
def get_expense(id):
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    for i in L:
        if i["id"]==id:
            return jsonify(i),200
    return jsonify({"Message":f"Expense with {id} not found"}),404
@app.route("/expenses",methods=["POST"])
def create_expense():
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    data=request.get_json(silent=True)
    try:
        expense=CreateExpense.model_validate(data)
    except ValidationError as e:
        return jsonify({"Error":str(e)}),400
    try:
        if expense.id in [i["id"] for i in L]:
            return jsonify({"Error":f"Expense with {expense.id} already exists"}),400
    except KeyError:
        pass
    expense_data=expense.model_dump()
    L.append(expense_data)
    return jsonify({"Message":"Created","Data":L}),201
@app.route("/expenses/<int:id>",methods=["PATCH"])
def patch_expense(id):
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    data=request.get_json(silent=True)
    try:
        expense=PatchExpense.model_validate(data)
    except ValidationError as e:
        return jsonify({"Error":str(e)}),400
    expense_data=expense.model_dump()
    update=None
    for i in L:
        if i["id"]==id:
            update=i
            break
    if update is not None:
        dictionary={}
        for i in expense_data:
            if expense_data[i] is None:
                dictionary[str(i)]=update[i]
            else:
                dictionary[str(i)]=expense_data[i]
        update.clear()
        update.update(dictionary)
        return jsonify({"Message":"Expense updated","Data":L}),200
    return jsonify({"Error":f"Expense with {id} not found"}),404
@app.route("/expenses/<int:id>",methods=["PUT"])
def update_expense(id):
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    data=request.get_json(silent=True)
    try:
        expense=PutExpense.model_validate(data)
    except ValidationError as e:
        return jsonify({"Error":str(e)}),400
    expense_data=expense.model_dump()
    update=None
    for i in L:
        if i["id"]==id:
            update=i
            break
    if update is not None:
        L.remove(update)
        L.append(expense_data)
        return jsonify({
            "Message":"Expense updated","Data":L}),200
    return jsonify({"Error":f"Expense with {id} not found"}),404
@app.route("/expenses/<int:id>",methods=["DELETE"])
def delete_expense(id):
    if not validate_api_key():
        return jsonify({"Error":"Invalid API Key"}),401
    for i in L:
        if i["id"]==id:
            L.remove(i)
            return jsonify({"Message":"Expense successfully deleted"}),200
    return jsonify({"Error":f"Expense with {id} not found"}),404
app.run(debug=True)