from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
import uuid
from rds.utils.base import Base, GUID


class Store(Base):
    __tablename__ = 'stores'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String)
    access_token = Column(String)
    email = Column(String)
    owner = Column(String)
    created_at = Column(Date)

    # Relación uno a muchos: una tienda puede tener varios productos
    products = relationship("Product", backref="store")
