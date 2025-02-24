import boto3
import json
import uuid
from datetime import datetime

# AWS Clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# AWS Resources
BUCKET_NAME = "corporate-file-uploads"  # Replace with your actual S3 bucket
DYNAMODB_TABLE = "FileUploads"  # Replace with your DynamoDB table name
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:FileUploadAlerts"  # Replace with your SNS topic ARN

def lambda_handler(event, context):
    """
    AWS Lambda function to:
    1. Upload files to S3
    2. Store metadata in S3
    3. Log details in DynamoDB
    4. Send an SNS notification
    """
    try:
        # Extract file details from the event
        file_source = event.get('source', 'Unknown')  # Email, FTP, API
        file_name = event.get('file_name', f"file_{uuid.uuid4().hex}.txt")
        file_content = event.get('content', "Sample corporate data").encode('utf-8')

        # Generate a unique File ID and timestamp
        file_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        # Define S3 object key
        s3_key = f"{file_source}/{timestamp}_{file_name}"

        # Upload file to S3 with metadata
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            Metadata={
                'Source': file_source,
                'FileID': file_id
            }
        )

        # Log file details in DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)
        table.put_item(
            Item={
                'FileID': file_id,
                'FileName': file_name,
                'UploadTime': timestamp,
                'Source': file_source,
                'S3Path': f"s3://{BUCKET_NAME}/{s3_key}"
            }
        )

        # Send SNS Notification
        sns_message = f"""
        File Upload Alert 
        File Name: {file_name}
        Source: {file_source}
        Upload Time: {timestamp}
        S3 Path: s3://{BUCKET_NAME}/{s3_key}
        """
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=sns_message,
            Subject="New File Uploaded to S3"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File uploaded, logged, and notification sent!',
                'file_id': file_id,
                'file_path': f"s3://{BUCKET_NAME}/{s3_key}",
                'source': file_source
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
