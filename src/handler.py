import json
import os
import boto3
from datetime import datetime, timezone
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    route = event.get("rawPath", "/")
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

    if route == "/hello" and method == "GET":
        return response(200, {"message": "Hello from API Gateway!"})

    elif route == "/items" and method == "GET":
        return get_items()

    elif route.startswith("/items/") and method == "GET":
        item_id = route.split("/")[-1]
        return get_item(item_id)

    elif route == "/items" and method == "POST":
        body = json.loads(event.get("body", "{}"))
        return create_item(body)

    elif route.startswith("/items/") and method == "DELETE":
        item_id = route.split("/")[-1]
        return delete_item(item_id)

    else:
        return response(404, {"error": "Route not found"})

def get_items():
    result = table.scan()
    return response(200, {"items": result.get("Items", [])})

def get_item(item_id):
    result = table.get_item(Key={"id": item_id})
    item = result.get("Item")
    if not item:
        return response(404, {"error": f"Item '{item_id}' not found"})
    return response(200, {"item": item})

def delete_item(item_id):
    result = table.get_item(Key={"id": item_id})
    item = result.get("Item")
    if not item:
        return response(404, {"error": f"Item '{item_id}' not found"})
    table.delete_item(Key={"id": item_id})
    return response(200, {"message": f"Item '{item_id}' deleted successfully"})
    
def create_item(body):
    name = body.get("name", "Unnamed")
    item = {
        "id": str(uuid.uuid4()),
        "name": name,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    table.put_item(Item=item)
    return response(201, {"message": "Item created successfully", "item": item})

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
