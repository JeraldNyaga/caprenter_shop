from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Furniture(Base):
    __tablename__ = 'furniture'

    furniture_id = Column(Integer, primary_key=True)
    carpenter_id = Column(Integer, ForeignKey('carpenters.carpenter_id'))
    furniture_name = Column(String(50), nullable=False)
    furniture_cost = Column(Float, nullable=False)
    color = Column(String(30))
    dimensions = Column(String(100))
    is_sold = Column(Boolean, default=False)

    carpenter = relationship("Carpenter", back_populates="furniture")
    order = relationship("CarpenterCustomer", back_populates="furniture", uselist=False)
