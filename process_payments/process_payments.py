from api.get_payments import get_all_payments
from api.filter_payments import filter_all_payments
from utils.send_email import send_email
from google_drive.update_google_sheet import update_google_sheet
import time


def process_payments(credentials, shop_name):
    try:
        print('Starting process_payments function', shop_name)
        # Obtener todos los pagos
        payments = get_all_payments(credentials)
        
        # Filtrar los pagos por producto
        totals_by_product = filter_all_payments(credentials, payments)

        for product_name, total in totals_by_product.items():
            success = False
            retries = 7
            while retries > 0 and not success:
                try:
                    print('Updating google sheet', product_name)
                    update_google_sheet(product_name, total, shop_name)
                    print('Update successful for', product_name)
                    success = True
                except Exception as e:
                    print(f"Error updating google sheet: {e}")
                    retries -= 1
                    print(f"Retrying updating google sheet for {product_name}. Retries left: {retries}")
                    time.sleep(60)

            if not success:
                print(f"Failed to update {product_name} after multiple attempts.")

        # Enviar un solo mensaje de correo electrónico con todos los totales
        message = f"Totales para {shop_name}:\n"
        for product_name, total in totals_by_product.items():
            message += f"{product_name}: ${total}\n"
        send_email(message, credentials['email'], shop_name)
        
        print('Finished process_payments function')
        return totals_by_product

    except Exception as e:
        raise Exception(f"Error in process_payments function: {e}")
