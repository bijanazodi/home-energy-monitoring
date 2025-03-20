import boto3
import csv
import json
from decimal import Decimal

# Initialize AWS clients
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("EnergyUsage")

def lambda_handler(event, context):
    try:
        print("Received Event:", json.dumps(event, indent=2))  # Debugging

        # Extract bucket name & file key from event
        bucket_name = event["bucket_name"]
        file_key = event["file_key"]

        # Fetch the CSV file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        content = response["Body"].read().decode("utf-8").splitlines()

        reader = csv.reader(content)
        next(reader)  # Skip header

        records = []
        for row in reader:
            date, usage = row
            item = {
                "userId": "default_user",  # Could be replaced by user auth later
                "date": date.strip(),
                "usage": Decimal(str(usage.strip()))  # Store as Decimal for DynamoDB
            }
            records.append(item)

        # Batch write to DynamoDB
        with table.batch_writer() as batch:
            for record in records:
                batch.put_item(Item=record)

        print("Successfully processed CSV file:", file_key)
        return {"statusCode": 200, "body": json.dumps({"message": "CSV data processed successfully"})}

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}
