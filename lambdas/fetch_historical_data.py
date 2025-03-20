import boto3
import json
from boto3.dynamodb.conditions import Key
from datetime import datetime
from decimal import Decimal

# Initialize AWS DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("EnergyUsage")

# Helper function to convert Decimal to float
def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def lambda_handler(event, context):
    try:
        print("Received Event:", json.dumps(event, indent=2))  # Debugging

        # Extract query parameters
        query_params = event.get("queryStringParameters", {})
        user_id = query_params.get("userId", "default_user")  # Default for now
        start_date = query_params.get("startDate")
        end_date = query_params.get("endDate")

        # Validate required parameters
        if not start_date or not end_date:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing required parameters: startDate and endDate"})}

        # Query DynamoDB for energy usage data
        response = table.query(
            KeyConditionExpression=Key("userId").eq(user_id) & Key("date").between(start_date, end_date)
        )

        items = response.get("Items", [])

        print("Fetched Records:", json.dumps(items, indent=2, default=decimal_to_float))  # Debugging

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Energy history retrieved successfully", "data": items},
                default=decimal_to_float  # Fixes serialization issue
            )
        }

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}
