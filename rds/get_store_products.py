from sqlalchemy.orm import sessionmaker
from rds.utils.db_connection import dev_engine, prod_engine
from rds.domain.product import Product
import os

STAGE = os.environ.get("STAGE")

if STAGE == "dev":
    engine = dev_engine
elif STAGE == "prod":
    engine = prod_engine

Session = sessionmaker(bind=engine)


def get_store_products_with_prices(store_id):
    with Session() as session:
        products = session.query(Product).filter(Product.store_id == store_id).all()
        products_list = []
        for product in products:
            # Asumiendo que 'prices' es una relación configurada en el modelo de Product
            # que devuelve todos los objetos Price asociados a este Product
            product_dict = {
                "name": product.name,
                "prices": [price.amount for price in product.prices]
            }
            products_list.append(product_dict)

    return products_list
