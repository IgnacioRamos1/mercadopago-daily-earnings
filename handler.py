from utils.utils import send_messages_to_sqs

from process_payments.process_payments import process_payments

import os
import logging
from datetime import datetime
import boto3
import json

from mongo_db.get_stores_id import get_stores_id
from mongo_db.get_store import get_store

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

sns_client = boto3.client('sns')

date = datetime.now().strftime('%Y-%m-%d')

stage = os.environ['STAGE']
sns_topic_arn = f'arn:aws:sns:sa-east-1:421852645480:MpLambdaErrorNotifications-{stage}'


def trigger_mp_processing(event, context):
    try:
        shop_ids = get_stores_id()
        
        # Enviar un mensaje a SQS por cada tienda
        send_messages_to_sqs(shop_ids)

        return {
            'statusCode': 200,
            'body': f"Triggered processing for {len(shop_ids)} shops."
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
            shop_id = message_body['shop_id']

            store = get_store(shop_id)

            # Procesar órdenes para esta tienda
            process_payments(store)
            print(f'Fin de procesamiento de tienda {store["name"]}')

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
            Subject=f'Error in process_shop function {date} - {store["name"]}'
        )
        return {
            'statusCode': 500,
            'body': str(e)
        }
