from datetime import datetime

class Comment():
  #intialise with database connection
  def __init__(self, db):
    self.db = db

  def create_comment(self, book_id, username, rating, text):
    comments = self.get_comments()

    #check if any comment exists else set last_id to 0
    if (len(comments) > 0):
      last_comment = comments[-1]
      last_id = last_comment['comment_id']
    else:
      last_id = 0

    time_now = datetime.now()

#    data = (int(last_id) + 1, book_id, username, str(datetime.now()), rating, text)
    data = (int(last_id) + 1, book_id, username, '{:%d/%m/%Y %H:%M}'.format(time_now), rating, text)

    self.db.cursor().execute('INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?)', data)
    self.db.commit()

  def get_book_comments(self, book_id, order = 'ASC'):
    comments = []

    if order == 'DESC':
      query = 'SELECT comment_id, username, time, rating, comment FROM comments WHERE book_id = ' + str(book_id) + ' ORDER BY comment_id DESC'
    else:
      query = 'SELECT comment_id, username, time, rating, comment FROM comments WHERE book_id = ' + str(book_id) + ' ORDER BY comment_id ASC'

    for row in self.db.cursor().execute(query):
      comment = {
        'comment_id' : row[0],
        'username' : row[1],
        'time' : row[2],
        'rating' : row[3],
        'comment' : row[4]
      }
      comments.append(comment)

    return comments

  def get_comment(self, comment_id):
    for row in self.db.cursor().execute('SELECT comment_id, username, time, rating, comment FROM comments WHERE comment_id = ' + str(comment_id)):
      comment = {
        'comment_id' : row[0],
        'username' : row[1],
        'time' : row[2],
        'rating' : row[3],
        'comment' : row[4]
      }

    return comment

  def get_comments(self):
    comments = []

    for row in self.db.cursor().execute('SELECT comment_id, username, time, rating, comment FROM comments'): 
      comment = {
        'comment_id' : row[0],
        'username' : row[1],
        'time' : row[2],
        'rating' : row[3],
        'comment' : row[4]
      }

      comments.append(comment)

    return comments
