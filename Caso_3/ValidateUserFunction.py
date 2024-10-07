import json

def lambda_handler(event, context):
    user_data = json.loads(event['body'])
    id = user_data.get('id')
    name = user_data.get('Name')
    email = user_data.get('Email')

    # Validar se todos os campos estão presentes
    if not id or not name or not email:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required fields'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(user_data)
    }
