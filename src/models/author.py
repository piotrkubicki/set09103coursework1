class Author():
  # initialise object with database connection
  def __init__(self, db):
    self.db = db

  def get_author(self, id):
    for row in self.db.cursor().execute('SELECT author_id, first_name, last_name, date_of_birth, date_of_dead FROM authors WHERE author_id=' + str(id)):
      author = {
        'id' : row[0],
        'first_name' : row[1],
        'last_name' : row[2],
        'date_of_birth' : row[3],
        'date_of_dead' : row[4]
      }

    return author

  def all(self):
    authors = []

    for row in self.db.cursor().execute('SELECT author_id, first_name, last_name, date_of_birth, date_of_dead FROM authors'):
      author = {
        'id' : row[0],
        'first_name' : row[1],
        'last_name' : row[2],
        'date_of_birth' : row[3],
        'date_of_dead' : row[4]
      }
      authors.append(author)

    return authors
