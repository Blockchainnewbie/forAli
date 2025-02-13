from table.ProductTable import ProductTable
from table.DBConnection import DBConnection
from sqlalchemy.exc import SQLAlchemyError
from helper.FormatCheck import FormatCheck
from interface.IModel import IModel
from sqlalchemy import update

class ProductModel(IModel):
    def __init__(self):
        self.Session = DBConnection.Session
    
    def create(self, name: str, description: str, price: float):
        self.__validateProductInfo(name=name, price=price)
        return self.__insert(name, description, price)
        
    def single(self, id: int) -> None|ProductTable:
        with self.Session() as session:
            try:
                return session.query(ProductTable).filter_by(id=id).first()
            except SQLAlchemyError as e:
                return {"error": f"Database failure: {str(e)}"}

    def list(self):
        with self.Session() as session:
            products = session.query(ProductTable).all()
            return [{"id": product.id, "name": product.name, "description": product.description, "price": product.price} for product in products]
    
    def update(self, product_id: int, name: str = None, description: str = None, price: float = None) -> ProductTable|None:
        product = self.single(product_id)
        if not product:
            return {"error": "Product not found"}
        
        if name or price:
            self.__validateProductInfo(name=name, price=price)

        with self.Session() as session:
            try:
                if name:
                    session.query(ProductTable).filter(ProductTable.id == product_id).update({
                        ProductTable.name: name
                    })
                if description is not None:
                    session.query(ProductTable).filter(ProductTable.id == product_id).update({
                        ProductTable.description: description
                    })
                if price:
                    session.query(ProductTable).filter(ProductTable.id == product_id).update({
                        ProductTable.price: price
                    })
                session.commit()
                return self.single(product_id)
            except SQLAlchemyError as e:
                session.rollback()
                return {"error": f"Database Error: {str(e)}"}

    def remove(self, id: int) -> bool:
        product = self.single(id)
        if not product:
            return {"error": "Product not found"}
        with self.Session() as session:
            try:
                session.delete(product)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                return False

    # Private Methods
    def __validateProductInfo(self, name: str = None, price: float = None):
        if name:
            if not FormatCheck.minimumLength(name, 2):
                return {"error": "Product name must have at least 2 characters"}
        if price is not None:
            if price < 0:
                return {"error": "Price cannot be negative"}
    
    def __insert(self, name: str, description: str, price: float):
        with self.Session() as session:
            try:
                new_product = ProductTable(name=name, description=description, price=price)
                session.add(new_product)
                session.commit()
                return {"created": "Product created successfully"}
            except SQLAlchemyError as e:
                return {"error": f"Database failure: {str(e)}"}