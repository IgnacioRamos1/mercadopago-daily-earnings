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
