from flask import Flask, g,  url_for, render_template
import sqlite3

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
  with app.app_context():
    db = get_db()
    with app.open_resource('database/schemas/genre_schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

    with app.open_resource('database/seeders/genres_seeder.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.route('/')
def index():
  db = get_db()
  #genres = ['Sci-fi', 'Drama', 'Comedy']
  genres = []
  sql = "SELECT name FROM genres"
  for row in db.cursor().execute(sql):
    genres.append(row[0])

  return render_template('layout.html', genres = genres)

if __name__ == '__main__':
  app.run('0.0.0.0', debug=True)
