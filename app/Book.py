import json


class Book:
    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description

    def __str__(self):
        return f"<b>{self.title}</b> - {self.author}<br>{self.description}"
    
class BooksDAO:
    def __init__(self, ruta_archivo: str):
        self.books = [ Book("Cien años de soledad", "Gabriel García Márquez", "La obra cumbre del realismo mágico que consolidó a García Márquez como una figura central de la literatura mundial.")
        ]
        self._ruta_archivo = ruta_archivo

    def get_books(self):
        return self.books

    def add_book(self, title, author, description):
        self.books.append(Book(title, author, description))
        return self.books

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]
        return self.books
    
    def save_books(self, books: list[Book]):
        books_data = [{'title': book.title, 'author': book.author, 'description': book.description} for book in books]
        with open(self._ruta_archivo, 'w', encoding='utf-8') as file:
            json.dump(books_data, file, ensure_ascii=False, indent=4)
        self.books = books
        return self.books
    
    def load_books(self):
        try:
            with open(self._ruta_archivo, 'r', encoding='utf-8') as file:
                books_data = json.load(file)
                return [Book(book['title'], book['author'], book['description']) for book in books_data]
        except FileNotFoundError:
            return []

    def update_book(self, title, author, description):
        for book in self.books:
            if book.title == title:
                book.author = author
                book.description = description
        return self.books

    def get_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None