class Book():
  # initialise object with database connection
  def __init__(self, db):
    self.db = db

  # return single book with given id
  def get_book(self, id):
    for row in self.db.cursor().execute('SELECT book_id, title, cover FROM books WHERE book_id=' + str(id)):
      book = {
        'id' : row[0],
        'title' : row[1],
        'cover' : row[2],
        'authors' :  self.get_authors(row[0])
      }

    return book

  # return book authors
  def get_authors(self, book_id):
    authors = []

    for author_id in self.db.cursor().execute('SELECT author_id FROM book_author WHERE book_id =' + str(book_id)):
      for author in self. db.cursor().execute('SELECT first_name, last_name FROM authors WHERE author_id =' + str(author_id[0])):
        authors.append(author[0] + ' ' + author[1])

    return authors

  # return all books from database
  def all(self):
    books = []
    for row in self.db.cursor().execute('SELECT book_id, title, cover FROM books'):
      book = {
        'id' : row[0],
        'title' : row[1],
        'cover' : row[2],
        'authors' :  self.get_authors(row[0])
      }
      books.append(book)

    return books
