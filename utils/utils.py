import boto3
import json
import os


def get_sqs_queue_url(queue_name):
    try:
        print('queue_name: ', queue_name)
        sqs = boto3.client('sqs')
        response = sqs.get_queue_url(QueueName=queue_name)
        return response['QueueUrl']

    except Exception as e:
        raise Exception(f"Error in get_sqs_queue_url function: {e}")


def send_messages_to_sqs(shop_names):
    try:
        sqs = boto3.client('sqs')
        queue_name = os.environ['SQS_QUEUE_NAME']
        queue_url = get_sqs_queue_url(queue_name)

        # Dividir shop_names en grupos de 10
        batches = [shop_names[i:i + 10] for i in range(0, len(shop_names), 10)]

        for batch in batches:
            entries = [{
                'Id': str(i),
                'MessageBody': json.dumps({"shop_name": name})
            } for i, name in enumerate(batch)]

            sqs.send_message_batch(QueueUrl=queue_url, Entries=entries)

    except Exception as e:
        raise Exception(f"Error in send_messages_to_sqs function: {e}")


def list_shop_secrets():
    try:
        client = boto3.client('secretsmanager', region_name='sa-east-1')
        response = client.list_secrets()

        shop_secrets = []
        for secret in response['SecretList']:
            if secret['Name'].startswith('shop_secret_'):
                shop_secrets.append(secret['Name'].replace('shop_secret_', ''))

        return shop_secrets

    except Exception as e:
        raise Exception(f"Error in list_shop_secrets function: {e}")


def get_secret(shop_name):
    try:
        client = boto3.client('secretsmanager', region_name='sa-east-1')
        response = client.get_secret_value(SecretId=shop_name)
        return json.loads(response['SecretString'])

    except Exception as e:
        raise Exception(f"Error in get_secret function: {e}")
