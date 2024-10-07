import json
import boto3

# Inicializa o cliente SNS
sns_client = boto3.client('sns')
topic_arn = 'arn:aws:sns:us-east-1:851725435807:Notification'

def lambda_handler(event, context):
    # Carrega os dados do usuário a partir do evento
    user_data = json.loads(event['body'])
    id = user_data['id']
    name = user_data['Name']
    email = user_data['Email']

    # Mensagem a ser enviada
    message = f"User {name} with ID {id} created successfully."

    try:

        # Envia notificação por e-mail através do tópico SNS
        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='User Creation Notification'
        )
        print("User data to be sent:", user_data)


        return {
            'statusCode': 200,
            'body': json.dumps(user_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to send notification',
                'details': str(e)
            })
        }
