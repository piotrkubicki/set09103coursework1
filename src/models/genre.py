from book import Book

class Genre():
  # initialise object with database connection
  def __init__(self, db):
    self.db = db

  #return single genre with given id
  def get_genre(self, id):
    for row in self.db.cursor().execute('SELECT genre_id, name FROM genres WHERE genre_id=' + str(id)):
      genre = {
        'id' : row[0],
        'name' : row[1]
      }

    return genre

  # return all genres from database
  def all(self):
    genres = []
    for row in self.db.cursor().execute('SELECT genre_id, name FROM genres'):
      genre = {
        'id' : row[0],
        'name' : row[1]
      }
      genres.append(genre)

    return genres

  # return all books for selected genre by genre id
  def get_books(self, genre_id):
    books = []
    book = Book(self.db)
    for row in self.db.cursor().execute('SELECT book_id FROM books WHERE genre_id=' + genre_id):
      books.append(book.get_book(row[0]))

    return books
