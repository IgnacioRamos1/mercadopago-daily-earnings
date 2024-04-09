from sqlalchemy.orm import sessionmaker
from manual.manual_product import Product, Price
from manual.manual_store import Store
from utils.db_connection import dev_engine, prod_engine

DevSession = sessionmaker(bind=dev_engine)
ProdSession = sessionmaker(bind=prod_engine)

dev_session = DevSession()
prod_session = ProdSession()

def migrate():
    # Migrar Stores
    for store_instance in dev_session.query(Store).all():
        prod_store = prod_session.merge(store_instance)
        prod_session.commit()
        
        # Migrar Products asociados a cada Store
        for product_instance in dev_session.query(Product).filter_by(store_id=store_instance.id).all():
            prod_product = prod_session.merge(product_instance)
            prod_session.commit()
            
            # Migrar Prices asociados a cada Product
            for price_instance in dev_session.query(Price).filter_by(product_id=product_instance.id).all():
                prod_session.merge(price_instance)
                prod_session.commit()


    # Eliminar Prices que ya no existen
    prod_price_ids = {price.id for price in prod_session.query(Price).all()}
    dev_price_ids = {price.id for price in dev_session.query(Price).all()}
    prices_to_delete_ids = prod_price_ids - dev_price_ids
    for price_id in prices_to_delete_ids:
        price_to_delete = prod_session.query(Price).get(price_id)
        if price_to_delete:
            prod_session.delete(price_to_delete)
            prod_session.commit()

    # Eliminar Products que ya no existen
    prod_product_ids = {product.id for product in prod_session.query(Product).all()}
    dev_product_ids = {product.id for product in dev_session.query(Product).all()}
    products_to_delete_ids = prod_product_ids - dev_product_ids
    for product_id in products_to_delete_ids:
        product_to_delete = prod_session.query(Product).get(product_id)
        if product_to_delete:
            prod_session.delete(product_to_delete)
            prod_session.commit()

    # Eliminar Stores que ya no existen
    prod_store_ids = {store.id for store in prod_session.query(Store).all()}
    dev_store_ids = {store.id for store in dev_session.query(Store).all()}
    stores_to_delete_ids = prod_store_ids - dev_store_ids
    for store_id in stores_to_delete_ids:
        store_to_delete = prod_session.query(Store).get(store_id)
        if store_to_delete:
            prod_session.delete(store_to_delete)
            prod_session.commit()

    dev_session.close()
    prod_session.close()

if __name__ == '__main__':
    migrate()
