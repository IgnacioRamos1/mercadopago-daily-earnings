from api.get_payments import get_all_payments
from api.filter_payments import filter_all_payments

def process_payments(credentials):
    try:
        # Obtener todos los pagos
        payments = get_all_payments(credentials)
        
        # Filtrar los pagos por producto
        totals_by_product = filter_all_payments(credentials, payments)
        
        print('totals_by_product: ', totals_by_product)
        return totals_by_product
    except Exception as e:
        raise Exception(f"Error in process_payments function: {e}")

