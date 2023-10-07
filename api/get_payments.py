import requests


def get_all_payments(credentials):
    try:
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {credentials["access_token"]}'
        }

        params = {
            'begin_date': '2023-10-01T04:00:00Z',
            'end_date': '2023-10-02T04:00:00Z',
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
