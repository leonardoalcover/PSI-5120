import json
import boto3
from decimal import Decimal

# Conexão com o DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    # Log do evento recebido
    print("Received event:", event)

    body = {}  # Dicionário para armazenar o corpo da resposta
    statusCode = 200  # Código de status HTTP padrão (200 OK)

    try:
        # Log da rota (método + endpoint) sendo usada
        print(f"Processing route: {event['routeKey']}")

        # Deletar um usuário pelo id
        if event['routeKey'] == "DELETE /users/{id}":
            id = event['pathParameters']['id']
            print(f"Deleting user with id: {id}")
            table.delete_item(Key={'id': id})
            body = f'Deleted user with UserId {id}'

        # Buscar um usuário específico pelo UserId
        elif event['routeKey'] == "GET /users/{id}":
            id = event['pathParameters']['id']
            print(f"Getting user with id: {id}")
            response = table.get_item(Key={'id': id})
            if 'Item' in response:
                user = response['Item']
                responseBody = {
                    'id': user['id'],
                    'Name': user['Name'],
                    'Email': user['Email'],
                    'Timestamp': user['timestamp']
                }
                body = responseBody
                print(f"Fetched user: {responseBody}")
            else:
                # Se o usuário não for encontrado
                statusCode = 404  # Not Found
                body = {'error': 'User not found'}

        # Buscar todos os usuários na tabela
        elif event['routeKey'] == "GET /users":
            print("Scanning all users in the table")
            response = table.scan()
            users = response["Items"]
            print(f"Users found: {users}")
            responseBody = []
            for user in users:
                responseItems = {
                    'id': user['id'],
                    'Name': user['Name'],
                    'Email': user['Email'],
                    'Timestamp': user['timestamp']
                }
                responseBody.append(responseItems)
            body = responseBody
            print(f"All users processed: {responseBody}")

        # Inserir um novo usuário
        elif event['routeKey'] == "POST /users":
            requestJSON = json.loads(event['body'])
            print(f"Inserting user with UserId: {requestJSON['id']}, Name: {requestJSON['Name']}, Email: {requestJSON['Email']}")
            table.put_item(
                Item={
                    'id': requestJSON['id'],
                    'Name': requestJSON['Name'],
                    'Email': requestJSON['Email'],
                    'timestamp': requestJSON.get('timestamp', 'N/A')  # Adicionar timestamp se fornecido
                })
            body = f'Inserted user with id {requestJSON["id"]}'

        # Atualizar um usuário existente
        elif event['routeKey'] == "PUT /users/{id}":
            id = event['pathParameters']['id']
            requestJSON = json.loads(event['body'])
            print(f"Updating user with id: {id}")

            # Construção da expressão de atualização dinamicamente, conforme os campos fornecidos
            update_expression = "SET "
            expression_attribute_values = {}
            expression_attribute_names = {}

            # Verificar se 'Name' foi enviado e adicionar à expressão de atualização
            if 'Name' in requestJSON:
                update_expression += "#N = :n, "
                expression_attribute_values[':n'] = requestJSON['Name']
                expression_attribute_names['#N'] = 'Name'

            # Verificar se 'Email' foi enviado e adicionar à expressão de atualização
            if 'Email' in requestJSON:
                update_expression += "#E = :e, "
                expression_attribute_values[':e'] = requestJSON['Email']
                expression_attribute_names['#E'] = 'Email'

            # Verificar se 'timestamp' foi enviado e adicionar à expressão de atualização
            if 'timestamp' in requestJSON:
                update_expression += "#T = :t, "
                expression_attribute_values[':t'] = requestJSON['timestamp']
                expression_attribute_names['#T'] = 'timestamp'

            # Remover a vírgula e espaço extra no final da expressão
            update_expression = update_expression.rstrip(', ')

            if update_expression:
                table.update_item(
                    Key={'id': id},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_attribute_values,
                    ExpressionAttributeNames=expression_attribute_names
                )
                body = f'Updated user with id {id}'
                print(f"Updated user: {id}")
            else:
                # Se nenhum campo válido for enviado para atualização
                statusCode = 400
                body = 'No valid fields to update'

    except KeyError as e:
        # Capturar e logar erros de chave faltante
        statusCode = 400
        body = f"Unsupported route: {event['routeKey']}. Error: {str(e)}"
        print(f"KeyError encountered: {str(e)}")

    except Exception as e:
        statusCode = 500  # Internal Server Error
        body = f"An error occurred: {str(e)}"
        print(f"Exception encountered: {str(e)}")

    print(f"Response: {body}")

    # Retornar a resposta final com status code, headers e body
    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

