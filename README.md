# Home Energy Monitoring App

## Overview
This project is a cloud-based home energy monitoring application that allows users to:
- Manually input daily energy usage.
- Upload CSV files for bulk energy tracking.
- View historical energy consumption trends.
- Receive alerts when energy usage exceeds predefined thresholds.

This application is built using **AWS Lambda, API Gateway, DynamoDB, S3, Cognito, and SNS**.

## Architecture
The system is designed using serverless architecture on AWS:
- **Amazon API Gateway**: Exposes RESTful API endpoints.
- **AWS Lambda**: Handles business logic for authentication, data storage, and alerts.
- **Amazon DynamoDB**: Stores energy usage data and user thresholds.
- **Amazon S3**: Stores uploaded CSV files for batch processing.
- **Amazon SNS**: Sends alerts when energy consumption exceeds thresholds.
- **Amazon Cognito**: Manages user authentication and access control.

## API Endpoints
| **Method** | **Endpoint**               | **Description** |
|------------|----------------------------|-----------------|
| **POST**   | `/auth/signup`              | Register a new user |
| **POST**   | `/auth/login`               | User login |
| **POST**   | `/energy/input`             | Manually input energy usage |
| **POST**   | `/energy/upload`            | Upload a CSV file containing energy usage |
| **GET**    | `/energy/history`           | View historical energy usage for a date range |
| **POST**   | `/alerts`                   | Set usage threshold and receive alerts |

---

## Deployment Instructions

### Prerequisites
- An **AWS account** with permissions to create Lambda functions, DynamoDB tables, API Gateway, S3 buckets, and SNS topics.
- **AWS CLI** installed and configured.
- **Postman** for API testing.
- **Python 3.12** installed.

### Step 1: Clone the Repository
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/home-energy-monitoring.git
cd home-energy-monitoring
```

### Step 2: Deploy AWS Infrastructure
1. **Create DynamoDB Table**
   ```sh
   aws dynamodb create-table --table-name EnergyUsage \
   --attribute-definitions AttributeName=userId,AttributeType=S \
   --key-schema AttributeName=userId,KeyType=HASH \
   --billing-mode PAY_PER_REQUEST
   ```

2. **Create S3 Bucket for File Uploads**
   ```sh
   aws s3api create-bucket --bucket home-energy-csv --region us-west-2
   ```

3. **Create an SNS Topic for Alerts**
   ```sh
   aws sns create-topic --name EnergyAlerts
   ```

### Step 3: Deploy Lambda Functions
1. **Package and Deploy Lambda Functions**
   ```sh
   zip user_auth_lambda.zip user_auth_lambda.py
   aws lambda update-function-code --function-name UserAuthLambda --zip-file fileb://user_auth_lambda.zip
   ```

   Repeat for all Lambda functions:
   ```sh
   zip process_csv_upload.zip process_csv_upload.py
   aws lambda update-function-code --function-name ProcessCSVUpload --zip-file fileb://process_csv_upload.zip
   ```

### Step 4: Configure API Gateway
1. **Create a new API in API Gateway**
2. **Define the routes** (`/auth/signup`, `/energy/input`, etc.)
3. **Link API routes to the respective Lambda functions**
4. **Deploy the API and note down the base URL**

---

## Testing the APIs in Postman
### 1. Sign Up a User
**Endpoint:** `POST /auth/signup`  
**Request Body:**
```json
{
    "email": "test@example.com",
    "password": "SecurePass123!"
}
```
**Response:**
```json
{
    "message": "User signed up successfully",
    "userId": "123e4567-e89b-12d3-a456-426614174000"
}
```

### 2. Log In a User
**Endpoint:** `POST /auth/login`  
**Request Body:**
```json
{
    "email": "test@example.com",
    "password": "SecurePass123!"
}
```
**Response:**
```json
{
    "message": "Login successful",
    "id_token": "eyJraWQiOiJ...",
    "access_token": "eyJraWQiOiJ..."
}
```

### 3. Manually Input Energy Data
**Endpoint:** `POST /energy/input`  
**Request Body:**
```json
{
    "userId": "testuser123",
    "date": "2024-06-10",
    "usage": 25.5
}
```
**Response:**
```json
{
    "message": "Energy data saved successfully"
}
```

### 4. Upload a CSV File
1. **Upload a CSV file to S3**
   - Ensure the file format:
   ```
   Date,Usage (kWh)
   2024-06-01,25.0
   2024-06-02,26.3
   ```
   - Upload the file using the API.

2. **Trigger CSV Processing Lambda**
   **Endpoint:** `POST /energy/upload`
   **Request Body:**
   ```json
   {
       "file_key": "test_upload.csv"
   }
   ```
   **Response:**
   ```json
   {
       "message": "CSV data processed successfully"
   }
   ```

### 5. Retrieve Historical Data
**Endpoint:** `GET /energy/history?startDate=2024-06-01&endDate=2024-06-10`  
**Response:**
```json
[
    {"date": "2024-06-01", "usage": 25.0},
    {"date": "2024-06-02", "usage": 26.3}
]
```

### 6. Set a Usage Threshold and Receive Alerts
**Endpoint:** `POST /alerts`  
**Request Body:**
```json
{
    "threshold": 30
}
```
**Response:**
```json
{
    "message": "Alerts sent successfully",
    "alerts": [
        "High energy usage detected for User test123 on 2024-06-10: 42.5 kWh."
    ]
}
```

---

## Security Considerations
- **AWS Cognito** is used for secure authentication.
- **API Gateway** requires authentication headers.
- **DynamoDB** access is controlled via IAM policies.
- **S3 bucket** is private, with permissions limited to the Lambda role.

---


