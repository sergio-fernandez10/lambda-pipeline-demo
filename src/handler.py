import json

def lambda_handler(event, context):
    route = event.get("rawPath", "/")
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    if route == "/hello" and method == "GET":
        return response(200, {"message": "Hello from API Gateway!"})

    elif route == "/items" and method == "GET":
        items = [
            {"id": 1, "name": "Item One"},
            {"id": 2, "name": "Item Two"},
            {"id": 3, "name": "Item Three"},
        ]
        return response(200, {"items":items})

    elif route == "/items" and method == "POST":
        body = json.loads(event.get("body", "{}"))
        name = body.get("name", "Unnamed")
        return response(201, {"message": f"Item '{name}' created successfully"})

    else:
        return response(404, {"error": "Route not found"})

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
