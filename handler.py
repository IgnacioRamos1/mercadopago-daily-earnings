from api.get_all_payments import get_all_payments
from utils.utils import send_messages_to_sqs, list_shop_secrets, get_secret

import os
import logging
from datetime import datetime
import boto3
import json


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

sns_client = boto3.client('sns')

date = datetime.now().strftime('%Y-%m-%d')

stage = os.environ['STAGE']
sns_topic_arn = f'arn:aws:sns:sa-east-1:421852645480:MpLambdaErrorNotifications-{stage}'


def trigger_mp_processing(event, context):
    try:
        # Obtener la lista de tiendas desde Secrets Manager
        shop_names = list_shop_secrets()

        # Enviar un mensaje a SQS por cada tienda
        send_messages_to_sqs(shop_names)

        return {
            'statusCode': 200,
            'body': f"Triggered processing for {len(shop_names)} shops."
        }
    except Exception as e:
        error_message = f'Error in trigger_shop_processing function: {e}'
        logger.error(error_message)

        # Publicar mensaje de error en SNS
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=error_message,
            Subject=f'Error in trigger_shop_processing function {date}'
        )

        return {
            'statusCode': 500,
            'body': str(e)
        }


def process_mp_shop(event, context):
    try:
        # Procesar cada mensaje en el evento de SQS
        for record in event['Records']:
            print('Inicio de procesamiento de tienda')
            message_body = json.loads(record['body'])
            shop_name = message_body['shop_name']

            # Recuperar las credenciales para esta tienda específica
            #credentials = get_secret(f'mp_secret_{shop_name}')
            # Procesar órdenes para esta tienda
            print(get_all_payments('credentials'))
            print('Fin de procesamiento de tienda')

        return {
            'statusCode': 200,
            'body': "CSV files generated and saved to S3"
        }
    except Exception as e:
        error_message = f'Error in process_shop function: {e}'
        logger.error(error_message)

        # Publicar mensaje de error en SNS
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=error_message,
            Subject=f'Error in process_shop function {date} - {shop_name}'
        )
        return {
            'statusCode': 500,
            'body': str(e)
        }
