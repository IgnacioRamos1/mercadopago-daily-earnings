from sqlalchemy import Column, Integer, String, ForeignKey, Float
import uuid
from sqlalchemy.orm import relationship
from rds.utils.base import Base, GUID


class Product(Base):
    __tablename__ = 'products'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)    
    store_id = Column(GUID, ForeignKey('stores.id'), nullable=False)
    name = Column(String)

    # Relación uno a muchos: un producto puede tener varios precios
    prices = relationship("Price", backref="product")


class Price(Base):
    __tablename__ = 'prices'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    product_id = Column(GUID, ForeignKey('products.id'), nullable=False)
    amount = Column(Float, nullable=False)  # El precio del producto
