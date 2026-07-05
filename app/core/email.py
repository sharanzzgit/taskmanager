import boto3
import json
import os

sqs = boto3.client(
    'sqs',
    region_name='ap-south-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

QUEUE_URL = os.getenv('SQS_QUEUE_URL')

async def send_task_email(email: str, task_title: str):
    if os.getenv("TESTING") == "1":
        return
    
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps({
            "email": email,
            "task_title": task_title
        })
    )