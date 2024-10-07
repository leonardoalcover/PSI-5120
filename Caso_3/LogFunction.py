import json
import boto3
from datetime import datetime

s3_client = boto3.client('s3')
bucket_name = 'alcoverbucket'

def lambda_handler(event, context):
    user_data = json.loads(event['body'])

    # Gerando nome único para o arquivo no S3
    timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f"user_{user_data['id']}_{timestamp}.json"

    # Criando o conteúdo do arquivo
    s3_data = {
        'id': user_data['id'],
        'Name': user_data['Name'],
        'Email': user_data['Email'],
        'Timestamp': timestamp
    }

    try:
        # Salvando no S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(s3_data),
            ContentType='application/json'
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f'User data saved to S3 as {file_name}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to save data to S3', 'details': str(e)})
        }
