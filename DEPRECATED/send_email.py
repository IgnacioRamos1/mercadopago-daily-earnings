import boto3
from utils.utils import get_parameter

from_email = get_parameter('from_email')


def send_email(message, email, shop_name):
    try:
        print('Starting send_email function')
        ses = boto3.client('ses', region_name='sa-east-1')

        subject = f"Totales para {shop_name}"
        body = message

        msg = {
            'Data': f"""Subject: {subject}
From: {from_email}
To: {email}
MIME-Version: 1.0
Content-type: text/plain
Content-Transfer-Encoding: 8bit

{body}
"""
        }

        response = ses.send_raw_email(
            Source=from_email,
            Destinations=[email],
            RawMessage=msg
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception(f"Error sending email: {response}")

        print('Finished send_email function')

        return response

    except Exception as e:
        raise Exception(f"Error in send_email function: {e}")
