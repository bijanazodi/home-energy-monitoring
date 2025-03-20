import boto3
import json
from decimal import Decimal

# 🔹 AWS Clients
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

# 🔹 DynamoDB Table & SNS Topic
TABLE_NAME = "EnergyUsage"
SNS_TOPIC_ARN = "arn:aws:sns:us-west-2:314146318953:EnergyAlerts"

# 🔹 Convert Decimal to Float (Fix JSON serialization issue)
def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj).__name__} is not JSON serializable")

def lambda_handler(event, context):
    try:
        print("Received Event:", json.dumps(event, indent=2))  # Debugging

        # Ensure request body is parsed properly
        body = None

        if "body" in event:
            try:
                body = json.loads(event["body"]) if event["body"] else {}
            except json.JSONDecodeError:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Invalid JSON format in request body"})
                }

        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing request body"})
            }

        # Extract threshold from the request body
        threshold = body.get("threshold")

        if threshold is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required parameter: threshold"})
            }

        threshold = Decimal(str(threshold))  # Convert to Decimal for DynamoDB

        # Scan DynamoDB for usage greater than threshold
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan()

        high_usage_records = [
            item for item in response.get("Items", []) if Decimal(item["usage"]) > threshold
        ]

        alerts = []
        for item in high_usage_records:
            user_id = item["userId"]
            date = item["date"]
            usage = float(item["usage"])  # Convert Decimal to Float
            
            alert_message = f" High energy usage detected for User {user_id} on {date}: {usage} kWh."
            alerts.append(alert_message)

            # Send SNS Alert
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=alert_message,
                Subject=" Energy Usage Alert"
            )

        if not alerts:
            return {"statusCode": 200, "body": json.dumps({"message": "No high usage detected."})}

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Alerts sent successfully", "alerts": alerts})
        }

    except Exception as e:
        print(" Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }
