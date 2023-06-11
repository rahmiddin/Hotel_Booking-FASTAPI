from app.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=True)
    image_id = Column(Integer)