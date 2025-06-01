from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Carpenter(Base):
    __tablename__ = 'carpenters'

    carpenter_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)

    furniture = relationship("Furniture", back_populates="carpenter")
    orders = relationship("CarpenterCustomer", back_populates="carpenter")
