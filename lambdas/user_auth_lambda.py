import boto3
import json
import base64
import hashlib
import hmac
import os

# Initialize Cognito Client
cognito_client = boto3.client('cognito-idp')

# Cognito User Pool Details with fillers
USER_POOL_ID = "us-west-2_RzWzglt2w"
CLIENT_ID = "1fu9qsuns3uuvkl13eapbn14ug"
CLIENT_SECRET = "1lnouq2b4nr3og89ifv24idhrjkqc7h1p3rl98f92356ovdmubto" 

def get_secret_hash(username):
    """Generate secret hash for Cognito authentication"""
    msg = username + CLIENT_ID
    dig = hmac.new(CLIENT_SECRET.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def lambda_handler(event, context):
    try:
        # Debug: Print received event
        print("Received Event:", json.dumps(event, indent=2))

        # Ensure JSON body exists
        body = json.loads(event['body']) if 'body' in event and event['body'] else {}

        # Check for required fields
        if "email" not in body or "password" not in body:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing email or password"})}

        email = body["email"].strip().lower()
        password = body["password"].strip()

        # Determine if this is signup or login
        if event["resource"] == "/auth/signup":
            return handle_signup(email, password)
        elif event["resource"] == "/auth/login":
            return handle_login(email, password)
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid action"})}

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}


def handle_signup(email, password):
    """Handles user signup"""
    try:
        # Check if user already exists
        try:
            cognito_client.admin_get_user(UserPoolId=USER_POOL_ID, Username=email)
            return {"statusCode": 409, "body": json.dumps({"error": "User already exists"})}
        except cognito_client.exceptions.UserNotFoundException:
            pass  # User does not exist, so we proceed with signup

        # Register user in Cognito
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            SecretHash=get_secret_hash(email),
            UserAttributes=[{"Name": "email", "Value": email}]
        )

        # Auto-confirm the user
        cognito_client.admin_confirm_sign_up(UserPoolId=USER_POOL_ID, Username=email)

        return {"statusCode": 201, "body": json.dumps({"message": "User signed up successfully", "userId": email})}

    except cognito_client.exceptions.UsernameExistsException:
        return {"statusCode": 409, "body": json.dumps({"error": "User already exists"})}
    except Exception as e:
        print("Signup Error:", str(e))
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}


def handle_login(email, password):
    """Handles user login"""
    try:
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
                "SECRET_HASH": get_secret_hash(email),
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Login successful",
                "id_token": response["AuthenticationResult"]["IdToken"],
                "access_token": response["AuthenticationResult"]["AccessToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"]
            })
        }

    except cognito_client.exceptions.NotAuthorizedException:
        return {"statusCode": 401, "body": json.dumps({"error": "Incorrect username or password"})}
    except cognito_client.exceptions.UserNotConfirmedException:
        return {"statusCode": 403, "body": json.dumps({"error": "User is not confirmed"})}
    except Exception as e:
        print("Login Error:", str(e))
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error", "details": str(e)})}
