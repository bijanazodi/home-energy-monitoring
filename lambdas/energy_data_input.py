import boto3
import json
from decimal import Decimal
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("EnergyUsage")

def lambda_handler(event, context):
    print("FULL EVENT RECEIVED:", json.dumps(event, indent=2))  # Debugging Step

    # Parse JSON if the request is wrapped in "body"
    if "body" in event:
        try:
            event = json.loads(event["body"])  # Extract actual JSON payload
        except json.JSONDecodeError:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON format"})}

    # Extract input parameters
    user_id = str(event.get("userId", "")).strip()  # Ensure it's a STRING & remove whitespace
    date = str(event.get("date", str(datetime.today().date()))).strip()  # Ensure date is STRING
    usage = event.get("usage")

    # Validate required fields
    if not user_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing required parameter: userId"})}

    if usage is None:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing required parameter: usage"})}

    # Convert usage to Decimal for DynamoDB
    try:
        usage = Decimal(str(usage))
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid format for usage, must be a number"})}

    # Create item to be saved
    item = {
        "userId": user_id,   
        "date": date,        
        "usage": usage       
    }

    # Debugging Step: Log exact structure before saving
    print("FINAL ITEM TO BE SAVED:", json.dumps(item, indent=2, default=str))

    # Save to DynamoDB
    try:
        response = table.put_item(Item=item)
        print("DynamoDB Response:", response)  # Log the DynamoDB response
    except Exception as e:
        print("DynamoDB Save Error:", str(e))  # Log exact error
        return {"statusCode": 500, "body": json.dumps({"error": "DynamoDB PutItem failed", "details": str(e)})}

    return {"statusCode": 201, "body": json.dumps({"message": "Energy data saved successfully"})}
