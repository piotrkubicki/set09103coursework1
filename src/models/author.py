class Author():
  def __init__(self, db):
    """Initialise object with database connection.

    Keyword arguments:
    db -- database connection
    """
    self.db = db

  def get_author(self, id):
    """Return author with given id."""
    for row in self.db.cursor().execute('SELECT author_id, first_name, last_name, date_of_birth, date_of_dead, photo FROM authors WHERE author_id=' + str(id)):
      author = {
        'id' : row[0],
        'first_name' : row[1],
        'last_name' : row[2],
        'date_of_birth' : row[3],
        'date_of_dead' : row[4],
        'photo' : row[5]
      }

    return author

  def all(self):
    """Returns all authors."""
    authors = []

    for row in self.db.cursor().execute('SELECT author_id, first_name, last_name, date_of_birth, date_of_dead, photo FROM authors'):
      author = {
        'id' : row[0],
        'first_name' : row[1],
        'last_name' : row[2],
        'date_of_birth' : row[3],
        'date_of_dead' : row[4],
        'photo' : row[5]
      }
      authors.append(author)

    return authors

  def get_books(self, id):
    """Returns all books for related with given authors id."""
    books = []

    book = Book(self.db)
    for book_id in self.db.cursor().execute('SELECT book_id FROM book_author WHERE author_id = ' + str(id)):
      books.append(book.get_book(book_id[0]))

    return books

  def search_for_books(self, query):
    """Returns list of books resulting from given query."""
    books = []
    book = Book(self.db)

    for author in self.db.cursor().execute('SELECT author_id FROM authors WHERE ' + query):
      books.extend(self.get_books(author[0]))

    return books


from book import Book
