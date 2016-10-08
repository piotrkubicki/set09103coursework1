from flask import Flask, g,  url_for, render_template, session, request
import sqlite3
from os import walk
from helpers.paginator import Paginator
from objects.book import Book
from objects.author import Author
from objects.genre import Genre

app = Flask(__name__)
app.secret_key = '^%&jjsh,H/Y?Tk*&^ll..l,kd(uTRv)*&'

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

  authors = Author(db).all()
  genres = Genre(db).all()
  books = Book(db).all()
  paginator = Paginator(books, 3, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator)

@app.route('/genre/<id>')
def search_by_genre(id):
  db = get_db()
  books = Genre(db).get_books(id)
  authors = Author(db).all()
  genres = Genre(db).all()

  return render_template('collection.html', genres = genres, authors = authors, books = books)

if __name__ == '__main__':
  app.run('0.0.0.0', debug=True)
