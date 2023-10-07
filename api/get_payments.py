import requests
import datetime


def get_all_payments(credentials):
    try:
        print('Start get_all_payments')
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {credentials["access_token"]}'
        }

        # Obtener la fecha actual
        today = datetime.datetime.utcnow().date()
        start_of_day = datetime.datetime.combine(today, datetime.time(4, 0)).isoformat() + 'Z'  # 04:00:00 del día actual
        end_of_day = datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time(4, 0)).isoformat() + 'Z'  # 04:00:00 del día siguiente

        params = {
            'begin_date': start_of_day,
            'end_date': end_of_day,
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
        print('Finished get_all_payments')
        return all_payments
    
    except Exception as e:
        raise Exception(f"Error in get_all_payments function: {e}")
