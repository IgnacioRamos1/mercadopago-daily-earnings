from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid
from rds.utils.base import Base, GUID


class Store(Base):
    __tablename__ = 'stores'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String)
    access_token = Column(String)
    email = Column(String)

    # Relación uno a muchos: una tienda puede tener varios productos
    products = relationship("Product", backref="store")
