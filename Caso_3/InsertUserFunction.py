import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    user_data = json.loads(event['body'])

    user_data['timestamp'] = datetime.utcnow().isoformat()  # Adicionando timestamp

    table.put_item(Item=user_data)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'id': user_data['id'],
            'Name': user_data['Name'],
            'Email': user_data['Email']
        })
    }
