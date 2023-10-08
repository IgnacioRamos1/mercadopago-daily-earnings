import requests
from utils.utils import get_parameter, ApiException
import os

token = get_parameter('whatsapp_token')
stage = os.environ['STAGE']


def send_whatsapp_message(body):
    try:
        print('Starting send_whatsapp_message function')
        url = "https://api.ultramsg.com/instance64344/messages/chat"
        if stage == 'dev':
            print('Sending whatsapp message to test group')
            # Si estamos en dev, enviar el mensaje al grupo de testeo
            chat_id = "120363150899530481@g.us"
        else:
            # Si estamos en prod, enviar el mensaje al grupo de producción
            chat_id = "5491166801711@c.us"

        payload = f"token={token}&to={chat_id}&body={body}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        if response.status_code != 200:
            raise ApiException(f"Error sending whatsapp message: {response.text}")

        print('Finished send_whatsapp_message function')

    except Exception as e:
        raise Exception(f"Error in send_whatsapp_message function: {e}")
