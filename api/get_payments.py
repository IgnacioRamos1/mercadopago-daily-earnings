import requests


def get_all_payments(credentials):
    try:
        print('Start get_all_payments')
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {credentials["access_token"]}'
        }

        params = {
            'begin_date': 'NOW-24HOURS',
            'end_date': 'NOW',
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
