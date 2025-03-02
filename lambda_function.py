import boto3
import pandas as pd
import uuid
from io import StringIO

# Initialize AWS clients
s3 = boto3.client('s3', endpoint_url="http://localhost:4566")
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

bucket_name = "csv-bucket"
file_name = "test.csv"
table_name = "UsersTable"

def lambda_handler():
    print("Lambda function is starting...")

    # Download the CSV file from S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    csv_content = obj['Body'].read().decode('utf-8')

    # Read CSV into DataFrame
    df = pd.read_csv(StringIO(csv_content))

    # Connect to the DynamoDB table
    table = dynamodb.Table(table_name)

    # Insert each row into DynamoDB
    for _, row in df.iterrows():
        table.put_item(
            Item={
                "id": str(uuid.uuid4()),  # Unique ID
                "name": row["name"],
                "age": int(row["age"]),
                "city": row["city"],
                "date": row["date"]
            }
        )

    print("Data successfully inserted into DynamoDB.")

# Run the function
lambda_handler()
