from process_payments.process_payments import process_payments
from utils.utils import send_messages_to_sqs

import os
import logging
from datetime import datetime
import boto3
import json

from rds.get_store_uuid import get_all_stores_uuid
from rds.get_store import get_store


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

sns_client = boto3.client('sns')

date = datetime.now().strftime('%Y-%m-%d')

stage = os.environ['STAGE']
sns_topic_arn = f'arn:aws:sns:sa-east-1:421852645480:MpLambdaErrorNotifications-{stage}'


def trigger_mp_processing(event, context):
    try:
        shop_uuids = get_all_stores_uuid()
        
        # Enviar un mensaje a SQS por cada tienda
        send_messages_to_sqs(shop_uuids)

        return {
            'statusCode': 200,
            'body': f"Triggered processing for {len(shop_uuids)} shops."
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
            shop_uuid = message_body['shop_uuid']

            store = get_store(shop_uuid)

            # Procesar órdenes para esta tienda
            process_payments(store)
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
            Subject=f'Error in process_shop function {date} - {store.name}'
        )
        return {
            'statusCode': 500,
            'body': str(e)
        }
