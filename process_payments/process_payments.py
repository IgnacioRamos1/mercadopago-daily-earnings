from api.get_payments import get_all_payments
from api.filter_payments import filter_all_payments
from utils.send_whatsapp_message import send_whatsapp_message


def process_payments(credentials, shop_name):
    try:
        # Obtener todos los pagos
        payments = get_all_payments(credentials)
        
        # Filtrar los pagos por producto
        totals_by_product = filter_all_payments(credentials, payments)

        # Enviar un mensaje de whatsapp con los totales
        message = f"Totales para {shop_name}:\n"
        for product_name, total in totals_by_product.items():
            message += f"{product_name}: ${total}\n"
        send_whatsapp_message(message)
        
        return totals_by_product

    except Exception as e:
        raise Exception(f"Error in process_payments function: {e}")
