from flask import Flask, g,  url_for, render_template
import sqlite3
from os import walk
from objects.book import Book

app = Flask(__name__)

db_location = 'database/books.db'

def get_db():
  db = getattr(g, 'db', None)
  if db is None:
    db = sqlite3.connect(db_location)
    g.db = db

  return db

@app.teardown_appcontext
def close_db_connection(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

def init_db():
  schemas = []
  seeders = []

  for (_, _, filenames) in walk('database/schemas/'):
    schemas.extend(filenames)

  for (_, _, filenames) in walk('database/seeders/'):
    seeders.extend(filenames)

  with app.app_context():
    db = get_db()
    print 'creating tables...'
    for schema in schemas:
      with app.open_resource('database/schemas/' + schema, mode='r') as f:
        db.cursor().executescript(f.read())
      db.commit()

    print 'tables created'

    print 'populating tables with seeds...'
    for seeder in seeders:
      print seeder
      with app.open_resource('database/seeders/' + seeder, mode='r') as f:
        db.cursor().executescript(f.read())
      db.commit()

    print 'tables seeded'

@app.route('/')
def index():
  db = get_db()
  authors = []
  genres = []
 # books = Book.all(db)
  books = []
  b = Book(db)
  for row in db.cursor().execute('SELECT name FROM genres'):
    genres.append(row[0])

  for row in db.cursor().execute('SELECT first_name, last_name FROM authors'):
    authors.append(row[0] + ' ' + row[1])

  #for row in db.cursor().execute('SELECT book_id, title, cover FROM books'):
  #  book = b.get_book(row[0])
  #  books.append(book)

  books = b.all()

  return render_template('collection.html', genres = genres, authors = authors, books = books)


if __name__ == '__main__':
  app.run('0.0.0.0', debug=True)
