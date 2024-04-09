import boto3
import json
import os

ssm_client = boto3.client('ssm')


class ApiException(Exception):
    pass


def get_parameter(name):
    """Retrieve a parameter from AWS Systems Manager Parameter Store."""
    try:
        response = ssm_client.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']

    except ssm_client.exceptions.ParameterNotFound:
        raise Exception(f"Parameter {name} not found in Parameter Store.")

    except ssm_client.exceptions.InternalServerError:
        raise Exception("Internal server error while fetching parameter from Parameter Store.")

    except Exception as e:
        raise Exception(f"Error retrieving parameter from Parameter Store: {e}")


def get_sqs_queue_url(queue_name):
    try:
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
                'MessageBody': json.dumps({"shop_uuid": name})
            } for i, name in enumerate(batch)]

            sqs.send_message_batch(QueueUrl=queue_url, Entries=entries)

    except Exception as e:
        raise Exception(f"Error in send_messages_to_sqs function: {e}")


def list_shop_secrets():
    try:
        client = boto3.client('secretsmanager', region_name='sa-east-1')
        paginator = client.get_paginator('list_secrets')
        shop_secrets = []

        # Itera a través de todas las páginas de la respuesta paginada
        for page in paginator.paginate():
            for secret in page['SecretList']:
                if secret['Name'].startswith('mp_secret_'):
                    shop_secrets.append(secret['Name'].replace('mp_secret_', ''))

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
