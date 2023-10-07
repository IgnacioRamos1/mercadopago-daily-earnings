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


def filter_all_payments(payments):
    products_values = {}
    counter = 0

    for payment in all_payments:
        print(payment)
        if 'shopify_data' in payment['metadata']:
            products_values[f'product_mail_{counter}'] = payment['metadata']['shopify_data']['customer']['email']
        products_values[f'product_value_{counter}'] = payment['transaction_details']['total_paid_amount']
        products_values[f'product_net_{counter}'] = payment['transaction_details']['net_received_amount']
        products_values[f'product_date_{counter}'] = payment['date_created'].split('T')[0]
        products_values[f'product_hour_{counter}'] = payment['date_created'].split('T')[1].split('.')[0]
        counter += 1


    print(products_values)
    print('-------------------')
    mail_counter = 0
    total_counter = 0
    for value in products_values:
        if 'product_mail' in value:
            mail_counter += 1
        total_counter += 1

    print('mail_counter: ', mail_counter)
    print('total_counter: ', total_counter)

    print('-------------------')

    counter = 0
    for value in products_values:
        if counter == len(products_values)/4 - 1:
            break
        print(products_values[f'product_net_{counter}'])
        counter += 1
