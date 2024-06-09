from api.get_payments import get_all_payments
from api.filter_payments import filter_all_payments
from google_drive.update_google_sheet import update_google_sheet
from mongo_db.utils.security import decrypt_string
from mongo_db.get_store_products import get_store_products


def process_payments(store):
    try:
        print('Starting process_payments function', store["name"])
        
        access_token = decrypt_string(store["access_token"])

        # Obtener todos los pagos
        payments = get_all_payments(access_token)

        products = get_store_products(store["_id"])
        
        # Filtrar los pagos por producto
        totals_by_product = filter_all_payments(products, payments)

        for product_name, total in totals_by_product.items():
            print(f"Updating spreadsheet for {product_name}")
            update_google_sheet(product_name, total, store["name"])
            print(f"Finished updating spreadsheet for {product_name}")
        
        print('Finished process_payments function')
        return totals_by_product

    except Exception as e:
        raise Exception(f"Error in process_payments function: {e}")
