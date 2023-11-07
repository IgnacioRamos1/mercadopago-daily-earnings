from api.get_payments import get_all_payments
from api.filter_payments import filter_all_payments
from utils.send_whatsapp_message import send_whatsapp_message
from google_drive.update_google_sheet import update_google_sheet
import os
import time

stage = os.environ['STAGE']


def process_payments(credentials, shop_name):
    try:
        print('Starting process_payments function', shop_name)
        # Obtener todos los pagos
        payments = get_all_payments(credentials)
        
        # Filtrar los pagos por producto
        totals_by_product = filter_all_payments(credentials, payments)

        try:
            for product_name, total in totals_by_product.items():
                print('Updating google sheet', product_name)
                update_google_sheet(product_name, total, shop_name)
                time.sleep(60)
        except Exception as e:
            # If it fails, continue with the process
            print(f"Error updating google sheet: {e}")
            print('Product Name', product_name)
        
        # Enviar un mensaje de whatsapp con los totales
        message = f"Totales para {shop_name}:\n"
        for product_name, total in totals_by_product.items():
            message += f"{product_name}: ${total}\n"
        send_whatsapp_message(message, credentials['wpp'])
        
        print('Finished process_payments function')
        return totals_by_product

    except Exception as e:
        raise Exception(f"Error in process_payments function: {e}")
