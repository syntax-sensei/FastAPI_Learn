from sqlalchemy import Boolean, Column, Integer, String, Float, Time, DateTime

from database import Base
    
class RestroBase(Base):
    __tablename__ = "restro"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    cuisine_type = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    phone_number = Column(String(15), nullable=False)
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    opening_time = Column(Time)
    closing_time = Column(Time)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<Restro(name={self.name}, cuisine_type={self.cuisine_type}, rating={self.rating})>"
