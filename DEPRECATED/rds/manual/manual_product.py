from sqlalchemy import Column, String, ForeignKey, Float
import uuid

import sys
import os
sys.path.append(os.path.abspath('..'))

from utils.base import Base, GUID


class Product(Base):
    __tablename__ = 'products'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)    
    store_id = Column(GUID, ForeignKey('stores.id'), nullable=False)
    name = Column(String)



class Price(Base):
    __tablename__ = 'prices'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    product_id = Column(GUID, ForeignKey('products.id'), nullable=False)
    amount = Column(Float, nullable=False)  # El precio del producto
