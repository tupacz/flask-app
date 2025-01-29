class Book:
    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description

    def __str__(self):
        return f"<b>{self.title}</b> - {self.author}<br>{self.description}"