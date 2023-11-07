import requests
from datetime import datetime, timedelta
import pytz


def get_all_payments(credentials):
    try:
        print('Start get_all_payments')
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {credentials["access_token"]}'
        }

        # Obtener la fecha y hora actual en la zona horaria de Argentina
        tz_argentina = pytz.timezone('America/Argentina/Buenos_Aires')

        # Obtener la fecha actual y calcular las fechas para el intervalo de búsqueda
        current_date = datetime.now(tz_argentina) - timedelta(days=1)  # Retrocede un día desde la fecha actual
        end_date = current_date.replace(hour=23, minute=59, second=59, microsecond=0)
        begin_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        params = {
            'begin_date': begin_date.strftime('%Y-%m-%dT%H:%M:%SZ'),  # Formato ISO8601
            'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),      # Formato ISO8601
            'limit': 100,
            'offset': 0
        }

        all_payments = []

        while True:
            response = requests.get('https://api.mercadopago.com/v1/payments/search', headers=headers, params=params)
            data = response.json()
            
            all_payments.extend(data['results'])

            # Si el número de resultados es menor que el límite, significa que ya no hay más pagos para obtener
            if len(data['results']) < params['limit']:
                break

            # Aumentar el offset para la próxima página
            params['offset'] += params['limit']
        return all_payments
    
    except Exception as e:
        raise Exception(f"Error in get_all_payments function: {e}")
