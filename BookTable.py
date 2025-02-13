from sqlalchemy import Column, Integer, String
from .DBConnection import Base

class BookTable(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    genre = Column(String, nullable=True)

    def __repr__(self):
        return f"Book(id='{self.id}', title='{self.title}', author='{self.author}', isbn='{self.isbn}', genre='{self.genre}')"