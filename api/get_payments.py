import mercadopago


def get_all_payments(access_token):
    try:
        print('Start get_all_payments')
        sdk = mercadopago.SDK(access_token)

        filters = {
            "sort": "date_created",
            "criteria": "desc",
            "range": "date_created",
            "begin_date": "NOW-2DAYS",
            "end_date": "NOW",
            "limit": 100,
            "offset": 0
        }

        all_payments = []

        while True:
           search_request = sdk.payment().search(filters)
           all_payments.extend(search_request['response']['results'])
           
           if len(search_request['response']['results']) < filters['limit']:
            break
           
           filters['offset'] += filters['limit']
        
        return all_payments
    
    except Exception as e:
        raise Exception(f"Error in get_all_payments function: {e}")
