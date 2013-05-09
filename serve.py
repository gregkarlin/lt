from bottle import route, run, template
from db import *

cur.execute('Select author,title FROM entry ORDER BY id DESC LIMIT 10;')
entries = cur.fetchall()

@route('/')
def index():
    return template('{{entries}}', entries=entries)

run(host='localhost', port=9980)


