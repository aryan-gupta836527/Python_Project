def validate_create_user(data):
    if not data:
        return "Request body is required"
    if "id" not in data:
        return "ID is required"
    if "name" not in data:
        return "Name is required"
    if not isinstance(data["id"], int):
        return "ID must be an integer"
    if not isinstance(data["name"], str):
        return "Name must be a string"
    if data["id"] <= 0:
        return "ID must be a positive integer"
    if len(data["name"].strip()) == 0:
        return "Name cannot be empty"
    return None
def validate_update_user(data):
    if not data:
        return "Request body is required"
    if "name" not in data:
        return "Name is required"
    if not isinstance(data["name"], str):
        return "Name must be a string"
    if len(data["name"].strip()) == 0:
        return "Name cannot be empty"
    return None