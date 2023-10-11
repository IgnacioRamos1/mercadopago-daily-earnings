

def filter_all_payments(credentials, payments):
    try:
        print('Starting filter_all_payments function')

        gross_amounts = []
        
        # Obtener la lista de productos desde Secrets Manager
        products = credentials['products']
        
        # Crear un diccionario para sumar los valores netos por producto
        totals_by_product = {}
        for product in products:
            totals_by_product[product['name']] = 0
        
        # Procesar cada pago
        for payment in payments:
            if 'shopify_data' in payment['metadata'] and payment['status'] == 'approved':
                gross_amount = payment['transaction_details']['total_paid_amount']
                net_amount = payment['transaction_details']['net_received_amount']

                gross_amounts.append(gross_amount)

                # Print email && date_created
                print(payment['payer']['email'], payment['date_created'], gross_amount, net_amount)

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
                else:
                    print(f"Warning: No product found for gross amount {gross_amount}!")
        
        # Redondear a dos decimales y agregar comas como separadores de miles
        for product_name, total in totals_by_product.items():
            totals_by_product[product_name] = "{:,.2f}".format(round(total, 2))

        print('Gross amounts', gross_amounts)
        print('Finished filter_all_payments function')
        return totals_by_product

    except Exception as e:
        raise Exception(f"Error in filter_all_payments function: {e}")
