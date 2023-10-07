
def filter_all_payments(credentials, payments):
    try:
        print('Starting filter_all_payments function')
        # Obtener la lista de productos desde Secrets Manager
        products = credentials['products']
        
        # Crear un diccionario para sumar los valores netos por producto
        totals_by_product = {}
        for product in products:
            totals_by_product[product['name']] = 0
        
        # Procesar cada pago
        for payment in payments:
            if 'shopify_data' in payment['metadata']:
                gross_amount = payment['transaction_details']['total_paid_amount']
                net_amount = payment['transaction_details']['net_received_amount']
                
                # Buscar el producto por el valor neto
                product_name = None
                for product in products:
                    if gross_amount in product['prices']:
                        product_name = product['name']
                        break
                if product_name:
                    totals_by_product[product_name] += net_amount
                else:
                    print(f"Warning: No product found for net amount {net_amount}!")
        
        # Redondear a dos decimales y agregar comas como separadores de miles
        for product_name, total in totals_by_product.items():
            totals_by_product[product_name] = "{:,.2f}".format(round(total, 2))

        print('Finished filter_all_payments function')
        return totals_by_product

    except Exception as e:
        raise Exception(f"Error in filter_all_payments function: {e}")