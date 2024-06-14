from datetime import datetime, timedelta


def filter_all_payments(products, payments, provider):
    try:
        print('Starting filter_all_payments function')

        gross_amounts = []
        net_amounts = []
        time = []
        
        # Crear un diccionario para sumar los valores netos por producto
        totals_by_product = {}
        for product in products:
            totals_by_product[product['name']] = 0
        
        # Procesar cada pago
        for payment in payments:
            if provider == 'shopify':
                if 'shopify_data' in payment['metadata'] and payment['status'] == 'approved':
                    filter_payments(payment, gross_amounts, net_amounts, time, products, totals_by_product)
            else:
                if 'shopify_data' in payment['metadata']:
                    continue
                if provider.replace(' ', '') in payment['metadata']['original_notification_url']:
                    counter = filter_payments(payment, gross_amounts, net_amounts, time, products, totals_by_product)
                    if counter == 1:
                        print(payment)
                        break               
        
        # Redondear a dos decimales y agregar comas como separadores de miles
        for product_name, total in totals_by_product.items():
            totals_by_product[product_name] = "{:,.2f}".format(round(total, 2))

        print('Net amounts', net_amounts)
        print('Gross amounts', gross_amounts)
        print('Time', time)
        print('Finished filter_all_payments function')
        return totals_by_product

    except Exception as e:
        raise Exception(f"Error in filter_all_payments function: {e}")


def filter_payments(payment, gross_amounts, net_amounts, time, products, totals_by_product):
    # Filtrar los pagos de ayer
    yesterday = datetime.now() - timedelta(days=1)
    date_created = datetime.strptime(payment['date_created'], "%Y-%m-%dT%H:%M:%S.%f%z")
    date_created = date_created.replace(tzinfo=None) + timedelta(hours=1) # Convertir a UTC-3

    if date_created.date() == yesterday.date():
        gross_amount = payment['transaction_details']['total_paid_amount']
        net_amount = payment['transaction_details']['net_received_amount']
        
        time.append(payment['date_created'])
        gross_amounts.append(gross_amount)
        net_amounts.append(net_amount)

        # Print email && date_created
        # print(payment['payer']['email'], payment['date_created'], gross_amount, net_amount)

        # Buscar el producto por el valor neto
        product_name = None
        for product in products:
            for price in product['prices']:
                # Verificar si el monto bruto es un múltiplo del precio
                if gross_amount % price == 0:
                    product_name = product['name']
                    break
            if product_name:
                break
        
        if product_name:
            totals_by_product[product_name] += net_amount
        
        return 1
