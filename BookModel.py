from table.BookTable import BookTable
from table.DBConnection import DBConnection
from sqlalchemy.exc import SQLAlchemyError
from helper.FormatCheck import FormatCheck
from interface.IModel import IModel
from sqlalchemy import update

class BookModel(IModel):
    def __init__(self):
        self.Session = DBConnection.Session
    
    def create(self, title: str, author: str, isbn: str, genre: str = None):
        self.__validateBookInfo(title=title, author=author, isbn=isbn)
        if self.singleByISBN(isbn):
            return {"error": "Book with this ISBN already exists"}
        return self.__insert(title, author, isbn, genre)
        
    def single(self, id: int) -> None|BookTable:
        with self.Session() as session:
            try:
                return session.query(BookTable).filter_by(id=id).first()
            except SQLAlchemyError as e:
                return {"error": f"Database failure: {str(e)}"}

    def singleByISBN(self, isbn: str) -> None|BookTable:
        with self.Session() as session:
            try:
                book = session.query(BookTable).filter_by(isbn=isbn).first()
                return {"id": book.id, "title": book.title, "author": book.author, "isbn": book.isbn, "genre": book.genre} if book else None
            except SQLAlchemyError as e:
                return {"error": f"Database failure: {str(e)}"}

    def list(self):
        with self.Session() as session:
            books = session.query(BookTable).all()
            return [{"id": book.id, "title": book.title, "author": book.author, "isbn": book.isbn, "genre": book.genre} for book in books]
    
    def update(self, book_id: int, title: str = None, author: str = None, genre: str = None) -> BookTable|None:
        book = self.single(book_id)
        if not book:
            return {"error": "Book not found"}
        
        if title or author:
            self.__validateBookInfo(title=title, author=author)

        with self.Session() as session:
            try:
                if title:
                    session.query(BookTable).filter(BookTable.id == book_id).update({
                        BookTable.title: title
                    })
                if author:
                    session.query(BookTable).filter(BookTable.id == book_id).update({
                        BookTable.author: author
                    })
                if genre is not None:
                    session.query(BookTable).filter(BookTable.id == book_id).update({
                        BookTable.genre: genre
                    })
                session.commit()
                return self.single(book_id)
            except SQLAlchemyError as e:
                session.rollback()
                return {"error": f"Database Error: {str(e)}"}

    def remove(self, id: int) -> bool:
        book = self.single(id)
        if not book:
            return {"error": "Book not found"}
        with self.Session() as session:
            try:
                session.delete(book)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                return False

    # Private Methods
    def __validateBookInfo(self, title: str = None, author: str = None, isbn: str = None):
        if title:
            if not FormatCheck.minimumLength(title, 1):
                return {"error": "Book title cannot be empty"}
        if author:
            if not FormatCheck.minimumLength(author, 2):
                return {"error": "Author name must have at least 2 characters"}
        if isbn:
            if not isbn.strip().replace("-", "").isalnum():
                return {"error": "Invalid ISBN format"}
    
    def __insert(self, title: str, author: str, isbn: str, genre: str):
        with self.Session() as session:
            try:
                new_book = BookTable(title=title, author=author, isbn=isbn, genre=genre)
                session.add(new_book)
                session.commit()
                return {"created": "Book created successfully"}
            except SQLAlchemyError as e:
                return {"error": f"Database failure: {str(e)}"}