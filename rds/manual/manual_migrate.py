from sqlalchemy.orm import sessionmaker

import sys
import os
sys.path.append(os.path.abspath('..'))

from utils.db_connection import dev_engine, prod_engine
from manual_store import Store
from manual_product import Product, Price


# Crear sesiones para desarrollo y producción
SessionDev = sessionmaker(bind=dev_engine)
SessionProd = sessionmaker(bind=prod_engine)


def migrate():
    session_dev = SessionDev()
    session_prod = SessionProd()

    stores_ids_dev = {store_instance.id for store_instance in session_dev.query(Store).all()}
    stores_ids_prod = {store_instance.id for store_instance in session_prod.query(Store).all()}

    stores_to_delete = stores_ids_prod - stores_ids_dev

    for store_id in stores_to_delete:
        products_to_delete = session_prod.query(Product).filter(Product.store_id == store_id).all()
        for product in products_to_delete:
            prices_to_delete = session_prod.query(Price).filter(Price.product_id == product.id).all()
            for price in prices_to_delete:
                session_prod.delete(price)
            session_prod.delete(product)
            
        store_to_delete = session_prod.query(Store).filter(Store.id == store_id).first()
        session_prod.delete(store_to_delete)
    
    for store_instance in session_dev.query(Store).all():
        session_prod.merge(store_instance)


    # Sync products
    products_ids_dev = {product_instance.id for product_instance in session_dev.query(Product).all()}
    products_ids_prod = {product_instance.id for product_instance in session_prod.query(Product).all()}

    products_to_delete = products_ids_prod - products_ids_dev

    for product_id in products_to_delete:
        prices_to_delete = session_prod.query(Price).filter(Price.product_id == product_id).all()
        for price in prices_to_delete:
            session_prod.delete(price)
        product_to_delete = session_prod.query(Product).filter(Product.id == product_id).first()
        session_prod.delete(product_to_delete)

    for product_instance in session_dev.query(Product).all():
        session_prod.merge(product_instance)
    

    # Sync prices
    prices_ids_dev = {price_instance.id for price_instance in session_dev.query(Price).all()}
    prices_ids_prod = {price_instance.id for price_instance in session_prod.query(Price).all()}

    prices_to_delete = prices_ids_prod - prices_ids_dev

    for price_id in prices_to_delete:
        price_to_delete = session_prod.query(Price).filter(Price.id == price_id).first()
        session_prod.delete(price_to_delete)

    for price_instance in session_dev.query(Price).all():
        session_prod.merge(price_instance)
    
    session_prod.commit()

    session_dev.close()
    session_prod.close()

    print("Migración completada con éxito.")

# Llamar a la función migrate
if __name__ == "__main__":
    migrate()
