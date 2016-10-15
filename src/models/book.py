class Book():
  # initialise object with database connection
  def __init__(self, db):
    self.db = db

  # return single book with given id
  def get_book(self, id):
    for row in self.db.cursor().execute('SELECT book_id, title, cover, publisher, pages, year FROM books WHERE book_id = ' + str(id)):
      book = {
        'id' : row[0],
        'title' : row[1],
        'cover' : row[2],
        'publisher' : row[3],
        'pages' : row[4],
        'year' : row[5],
        'authors' : self.get_authors(row[0])
      }

    return book

  # return book authors
  def get_authors(self, book_id):
    authors = []
    author = Author(self.db)

    for author_id in self.db.cursor().execute('SELECT author_id FROM book_author WHERE book_id =' + str(book_id)):
      authors.append(author.get_author(author_id[0]))

    return authors

  # return all books from database
  def all(self):
    books = []
    for row in self.db.cursor().execute('SELECT book_id, title, cover, publisher, pages, year FROM books'):
      book = {
        'id' : row[0],
        'title' : row[1],
        'cover' : row[2],
        'publisher' : row[3],
        'pages' : row[4],
        'year' : row[5],
        'authors' : self.get_authors(row[0])
      }
      books.append(book)

    return books

  # return all books for given search string
  def search(self, query):
    books = []

    for row in self.db.cursor().execute('SELECT book_id, title, cover, publisher, pages, year FROM books WHERE ' + query):
      book = {
        'id' : row[0],
        'title' : row[1],
        'cover' : row[2],
        'publisher' : row[3],
        'pages' : row[4],
        'year' : row[5],
        'authors' : self.get_authors(row[0])
      }
      books.append(book)

    return books

from author import Author
