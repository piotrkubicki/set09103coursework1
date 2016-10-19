class Genre():
  def __init__(self, db):
    """Initialize object with database connection.

    Keyword arguments:
    db -- database connection
    """
    self.db = db

  def get_genre(self, id):
    """Return single genre with given id."""
    for row in self.db.cursor().execute('SELECT genre_id, name FROM genres WHERE genre_id=' + str(id)):
      genre = {
        'id' : row[0],
        'name' : row[1]
      }

    return genre

  def all(self):
    """Return all genres from database."""
    genres = []
    for row in self.db.cursor().execute('SELECT genre_id, name FROM genres'):
      genre = {
        'id' : row[0],
        'name' : row[1]
      }
      genres.append(genre)

    return genres

  def get_books(self, genre_id):
    """Return all books for selected genre by genre id."""
    books = []
    book = Book(self.db)
    for row in self.db.cursor().execute('SELECT book_id FROM books WHERE genre_id=' + str(genre_id)):
      books.append(book.get_book(row[0]))

    return books

  def search_for_books(self, query):
    """Returns list of books resulting from given query."""
    books = []
    book = Book(self.db)
    for row in self.db.cursor().execute('SELECT genre_id FROM genres WHERE ' + query):
      books.extend(self.get_books(row[0]))

    return books

  def create_genre(self, name):
    """Add new genre to database."""
    genres = self.all()

    if len(genres) > 0:
      last_genre = genres[-1]
      last_id = last_genre['id']
    else:
      last_id = 0

    data = (int(last_id) + 1, name)

    self.db.cursor().execute('INSERT INTO genres VALUES (?, ?)', data)
    self.db.commit()

from book import Book
