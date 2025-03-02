# CSV Processor Lambda Setup

This document provides instructions to set up the CSV Processor Lambda function, which processes CSV files and stores data in DynamoDB.

## Prerequisites

- AWS CLI installed and configured
- LocalStack installed and running


## Setup Instructions

### 1. Start LocalStack

Start LocalStack using the following command:

```sh
localstack start
```

### 2. Create an S3 Bucket

Create an S3 bucket to store the CSV files:

```sh
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-csv-bucket
```

### 3. Create a DynamoDB Table

Create a DynamoDB table to store the processed data:

```sh
aws --endpoint-url=http://localhost:4566 dynamodb create-table --table-name UserData \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

### 4. Package Lambda Function

Package the Lambda function code:

```sh
zip function.zip index.js
```

### 5. Deploy Lambda Function

Deploy the Lambda function to LocalStack:

```sh
aws --endpoint-url=http://localhost:4566 lambda create-function --function-name CSVProcessor \
    --zip-file fileb://function.zip --handler index.handler --runtime nodejs14.x \
    --role arn:aws:iam::000000000000:role/lambda-role
```

### 6. Permission for S3 to Invoke Lambda

Grant S3 permission to invoke the Lambda function:

```sh
aws --endpoint-url=http://localhost:4566 lambda add-permission --function-name CSVProcessor \
    --principal s3.amazonaws.com --statement-id some-unique-id --action "lambda:InvokeFunction" \
    --source-arn arn:aws:s3:::my-csv-bucket
```

### 7. Configure S3 Event Notification

Configure S3 to trigger the Lambda function on object creation:

```sh
aws --endpoint-url=http://localhost:4566 s3api put-bucket-notification-configuration --bucket my-csv-bucket \
    --notification-configuration file://notification.json
```

### 8. Verify Setup

Upload a CSV file to the S3 bucket and verify that the data is processed and stored in DynamoDB:

```sh
aws --endpoint-url=http://localhost:4566 s3 cp test.csv s3://my-csv-bucket/test.csv
```

Check the DynamoDB table for the processed data:

```sh
aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name UserData
```

## Screenshots



(../Pictures/Screenshots/Screenshot%20from%202025-03-02%2018-08-50.png)



(../Pictures/Screenshots/Screenshot%20from%202025-03-02%2018-16-59.png)



(../Pictures/Screenshots/Screenshot%20from%202025-03-02%2018-17-42.png)



(../Pictures/Screenshots/Screenshot%20from%202025-03-02%2018-55-19.png)