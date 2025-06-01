from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(50), nullable=False)

    orders = relationship("CarpenterCustomer", back_populates="customer")
