from fastapi import FastAPI, HTTPException
import boto3
from botocore.exceptions import BotoCoreError, ClientError

app = FastAPI()

# Initialize the DynamoDB resource (ensure your AWS credentials/region are properly configured)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = "test-dynamodb"  # Replace with your actual table name

@app.get("/dynamodb")
def call_dynamodb():
    try:
        table = dynamodb.Table(table_name)
        # For demonstration, scan the table and return at most one item
        response = table.scan(Limit=3)
        items = response.get('Items', [])
        if items:
            return {"message": "Data retrieved from DynamoDB", "data": items}
        else:
            return {"message": "No data found in DynamoDB."}
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"Error accessing DynamoDB: {str(e)}")
