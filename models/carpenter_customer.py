from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class CarpenterCustomer(Base):
    __tablename__ = 'carpenter_customer'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    carpenter_id = Column(Integer, ForeignKey('carpenters.carpenter_id'))
    furniture_id = Column(Integer, ForeignKey('furniture.furniture_id'))
    time_ordered = Column(DateTime, default=datetime.utcnow)
    returned = Column(Boolean, default=False)
    remake_done = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="orders")
    carpenter = relationship("Carpenter", back_populates="orders")
    furniture = relationship("Furniture", back_populates="order")
