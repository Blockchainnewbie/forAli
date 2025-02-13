from sqlalchemy import Column, Integer, String, Float
from .DBConnection import Base

class ProductTable(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"Product(id='{self.id}', name='{self.name}', description='{self.description}', price='{self.price}')"