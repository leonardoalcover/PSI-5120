import boto3
import json

# Cria um cliente Lambda
lambda_client = boto3.client('lambda')

# Define o payload
payload = {
    "body": json.dumps({
        "UserId": "000000",
        "Name": "Joao",
        "Email": "joao@example.com"
    })
}

try:
    # Chama a função Lambda
    response = lambda_client.invoke(
        FunctionName='InsertUserFunction',  # Nome da sua função Lambda
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    # Lê a resposta
    response_payload = response['Payload'].read().decode('utf-8')
    print("Response from Lambda:", response_payload)

except Exception as e:
    print("Error calling Lambda:", e)
