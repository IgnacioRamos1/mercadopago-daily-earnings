import requests
from datetime import datetime, timedelta
import pytz


def get_all_payments(access_token):
    try:
        print('Start get_all_payments')
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        # Obtener la fecha y hora actual en la zona horaria 'America/New_York' (UTC-4)
        tz_new_york = pytz.timezone('America/New_York')
        current_date_new_york = datetime.now(tz_new_york)

        # Ajustar las horas, minutos y segundos para obtener el inicio y fin del día anterior en 'America/New_York' (UTC-4)
        end_date_new_york = current_date_new_york.replace(hour=0, minute=0, second=0, microsecond=0)
        begin_date_new_york = end_date_new_york - timedelta(days=1)

        # Convertir las fechas a la zona horaria de Argentina (UTC-3)
        tz_argentina = pytz.timezone('America/Argentina/Buenos_Aires')
        begin_date_argentina = begin_date_new_york.astimezone(tz_argentina) + timedelta(hours=2)
        end_date_argentina = end_date_new_york.astimezone(tz_argentina) + timedelta(hours=2)

        # Utilizar las fechas para la búsqueda en la API
        params = {
            'begin_date': begin_date_argentina.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'end_date': end_date_argentina.strftime('%Y-%m-%dT%H:%M:%SZ'),
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
