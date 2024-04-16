from sqlalchemy import Column, String, Date
import uuid

import sys
import os
sys.path.append(os.path.abspath('..'))

from utils.base import Base, GUID


class Store(Base):
    __tablename__ = 'stores'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String)
    access_token = Column(String)
    email = Column(String)
    owner = Column(String)
    created_at = Column(Date)

