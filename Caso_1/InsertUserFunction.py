import json
import boto3
from datetime import datetime

# Inicializando o recurso do DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    # Extraindo dados do corpo da requisição (evento)
    user_data = json.loads(event['body'])

    # Adicionando um campo de timestamp
    user_data['timestamp'] = datetime.utcnow().isoformat()

    try:
        # Inserindo os dados do usuário na tabela
        table.put_item(Item=user_data)

        # Retornando sucesso
        return {
            'statusCode': 200,
            'body': json.dumps('User inserted successfully')
        }
    except Exception as e:
        # Retornando erro
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Could not insert user',
                'details': str(e)
            })
        }
