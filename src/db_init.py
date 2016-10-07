from subprocess import call
from app import init_db

#create empty database file
call(['touch', 'database/books.db'])
print 'database created'
init_db()
print 'done!'
