from flask import Flask, g,  url_for, render_template, session, request, jsonify, redirect
import sqlite3
from functools import wraps
import base64
from os import walk
from helpers.paginator import Paginator
from models.book import Book
from models.author import Author
from models.genre import Genre
from models.comment import Comment

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

  for _, _, filenames in walk('database/schemas/'):
    schemas.extend(filenames)

  for _, _, filenames in walk('database/seeders/'):
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

def authenticate(username, password):
  if username == 'admin' and password == 'password':
    return True
  else:
    return False

def require_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    username = ''
    password = ''
    try:
      if (session['username']):
        username = str(session['username'])

      if (session['password']):
        password = str(session['password'])
    except KeyError:
      pass

    if not authenticate(username, password):
      return redirect(url_for('login'))

    return f(*args, **kwargs)

  return decorated

@app.errorhandler(404)
def page_not_found(error):
  return render_template('404_page.html'), 404

@app.route('/')
def index():
  db = get_db()

  authors = Author(db).all()
  genres = Genre(db).all()
  books = Book(db).all()
  paginator = Paginator(books, 10, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator)

@app.route('/search/')
def search():
  words = request.args.get('q', '')
  filters = request.args.get('filters', '').split()
  db = get_db()
  books = search_for_books(words, filters)
  authors = Author(db).all()
  genres = Genre(db).all()
  paginator = Paginator(books, 10, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator)

@app.route('/genres/<id>')
def search_by_genre(id):
  db = get_db()
  books = Genre(db).get_books(id)
  authors = Author(db).all()
  genres = Genre(db).all()
  paginator = Paginator(books, 10, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator, genre_id = int(id))

@app.route('/authors/<id>')
def search_by_author(id):
  db = get_db()
  books = Author(db).get_books(id)
  authors = Author(db).all()
  genres = Genre(db).all()
  paginator = Paginator(books, 10, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator, author_id = int(id))

@app.route('/books/<id>')
def show_book(id):
  db = get_db()
  authors = Author(db).all()
  genres = Genre(db).all()
  book = Book(db).get_book(id)
  comment = Comment(db)
  comments = comment.get_book_comments(id, 'DESC')
  votes = len(comments)
  rating = calculate_rating(comments, votes)

  return render_template('item_view.html', genres = genres, authors = authors, book = book, comments = comments, rating = rating, votes = votes)

@app.route('/books/<id>/comment', methods=['POST'])
def send_comment(id):
  db = get_db()
  comment = Comment(db)
  book_id = id
  username = request.json['username']
  rating = request.json['rating']
  text = request.json['text']
  response = {}

  if username == '' or rating == '' or text == '':
    response = {
      'error' : '<div class="alert alert-danger error active">All fields are required!</div>'
    }
  else:
    comment.create_comment(book_id, username, rating, text)
    comments = comment.get_book_comments(book_id, 'DESC')
    last_comment = comments[0]
    votes = len(comments)

    response = {
      'rate' : render_template('book_rate.html', rating = calculate_rating(comments, votes), votes = votes),
      'comments' : render_template('comment.html', comment = last_comment)
    }

  return jsonify(**response)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  else:
    username = request.form['username']
    password = request.form['password']

    if authenticate(username, password):
      session['username'] = username
      session['password'] = password

      return redirect(url_for('admin_root'))
    else:
      return redirect(url_for('login'))

@app.route('/logout/')
def logout():
  session.pop('username', None)
  session.pop('password', None)

  return redirect(url_for('login'))

@app.route('/admin/')
@require_auth
def admin_root():
  db = get_db()

  authors = Author(db).all()
  genres = Genre(db).all()
  books = Book(db).all()
  paginator = Paginator(books, 10, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator, admin = True)

@app.route('/admin/genre/', methods = ['POST'])
@require_auth
def create_genre():
  db = get_db()

  genre_name = request.json['name']

  if genre_name == '':
    response = {
      'error' : 'Please fill in all required fields!'
    }
  else:
    Genre(db).create_genre(genre_name)
    genres = Genre(db).all()
    last_genre = genres[-1]
    genre_id = str(last_genre['id'])
    response = {
      'success' : '<li class="list-item sublist-item" style="display: none"><a id=' + genre_id + '" href="/genres/' + genre_id + '/">' + genre_name + '</a></li>',
      'listentry' : '<option value="' + genre_id +'">' + genre_name + '</option>'
    }

  return jsonify(**response)

@app.route('/admin/author/', methods = ['POST'])
@require_auth
def create_author():
  db = get_db()
  first_name = request.json['first_name']
  last_name = request.json['last_name']
  dob = request.json['dob']
  dod = request.json['dod']
  photo = request.json['photo']

  if first_name == '' or last_name == '' or dob == '' or photo == '':
    response = {
      'error' : 'Please fill in all required fields!'
    }
  else:
    Author(db).create_author(first_name, last_name, dob, dod, photo)

    authors = Author(db).all()
    last_author = authors[-1]
    author_id = str(last_author['id'])

    response = {
      'success' : '<li class="list-item sublist-item" style="display: none"><a id=' + author_id + '" href="/genres/' + author_id + '/">' + first_name + ' ' + last_name + '</a></li>',
      'listentry' : '<option value="' + author_id + '">' + first_name + ' ' + last_name + '</option>'
    }

  return jsonify(**response)

@app.route('/admin/book/', methods = ['POST'])
@require_auth
def create_book():
  db = get_db()
  title = request.json['title']
  publisher = request.json['publisher']
  year = request.json['year']
  genre_id = request.json['genre_id']
  pages = request.json['pages']
  description = request.json['description']
  authors = request.json['authors']
  cover = request.json['photo']

  if title == '' or publisher == '' or year == '' or genre_id == '' or pages == '' or authors == [] or cover == '':
    response = {
      'error' : 'Please fill in all required fields!'
    }
  else:
    Book(db).create_book(title, year, publisher, cover, genre_id, pages, description, authors)
    books = Book(db).all()
    paginator = Paginator(books, 10, int(request.args.get('page', 1)))

    response = {
      'success' : render_template('books-collection.html', books = paginator.items, paginator = paginator)
    }

  return jsonify(**response)

@app.route('/admin/search/')
@require_auth
def admin_search():
  words = request.args.get('q', '')
  filters = request.args.get('filters', '').split()
  db = get_db()
  books = search_for_books(words, filters)
  authors = Author(db).all()
  genres = Genre(db).all()
  paginator = Paginator(books, 10, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator, admin = True)

@app.route('/admin/genres/<id>')
@require_auth
def admin_search_by_genre(id):
  db = get_db()
  books = Genre(db).get_books(id)
  authors = Author(db).all()
  genres = Genre(db).all()
  paginator = Paginator(books, 10, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator, genre_id = int(id), admin = True)

@app.route('/admin/authors/<id>')
@require_auth
def admin_search_by_author(id):
  db = get_db()
  books = Author(db).get_books(id)
  authors = Author(db).all()
  genres = Genre(db).all()
  paginator = Paginator(books, 10, int(request.args.get('page', 1)))

  return render_template('collection.html', genres = genres, authors = authors, books = paginator.items, paginator = paginator, author_id = int(id), admin = True)

@app.route('/admin/books/<id>')
def admin_show_book(id):
  db = get_db()
  authors = Author(db).all()
  genres = Genre(db).all()
  book = Book(db).get_book(id)
  comment = Comment(db)
  comments = comment.get_book_comments(id, 'DESC')
  votes = len(comments)
  rating = calculate_rating(comments, votes)

  return render_template('item_view.html', genres = genres, authors = authors, book = book, comments = comments, rating = rating, votes = votes, admin = True)

def calculate_rating(comments, votes):
  rating = 0

  if votes > 0:
    ratings = {
      'one_star' : 0,
      'two_stars' : 0,
      'three_stars' : 0,
      'four_stars' : 0,
      'five_stars' : 0
    }

    for rate in comments:
      if rate['rating'] == 1:
        ratings['one_star'] += 1
      elif rate['rating'] == 2:
        ratings['two_stars'] += 1
      elif rate['rating'] == 3:
        ratings['three_stars'] += 1
      elif rate['rating'] == 4:
        ratings['four_stars'] += 1
      else:
        ratings['five_stars'] += 1

    rating = (5 * ratings['five_stars'] + 4 * ratings['four_stars'] + 3 * ratings['three_stars'] + 2 * ratings['two_stars'] + ratings['one_star']) / float(votes)

  return rating

def create_search_query(words, *filters):
  """Form a query string. Return a string.

  Keyword arguments:
  words -- string containing words to search with special marks
  *filters -- tuple containing filters for search query
  """
  if not filters:
    filters = filters + ('title',)

  query = ''

  for filter in filters:
    query += filter + ' LIKE "%'

    for letter in words:
      if letter == '%':
        letter = '%" AND ' + filter + ' LIKE "%'
      elif letter == ' ':
        letter = '%" OR ' + filter + ' LIKE "%'

      query += letter

    if filter == filters[-1]:
      query += '%"'
    else:
      query += '%" OR '

  return query

def search_for_books(words, filters):
  """Return a list of books for all given words and filters

  Keyword arguments:
  words -- string containing words to search
  filters -- list of strings
  """
  db = get_db()
  books = {}

  if not filters:
    filters.append('title')

  for filter in filters:
    if filter == 'title':
      temp = Book(db).search(create_search_query(words))
      for book in temp:
        books[book['id']] = book
    elif filter == 'author':
      temp = Author(db).search_for_books(create_search_query(words, 'first_name', 'last_name'))
      for book in temp:
        if book['id'] not in books:
          books[book['id']] = book
    elif filter == 'genre':
      temp = Genre(db).search_for_books(create_search_query(words, 'name'))
      for book in temp:
        if book['id'] not in books:
          books[book['id']] = book

  return [book for book in books.values()]


if __name__ == '__main__':
  app.run('0.0.0.0', debug=True)
