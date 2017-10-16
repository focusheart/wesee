'''
WeSee Server
'''
import os
import sqlite3
import ConfigParser
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify, send_from_directory

DEBUG = True
HOST = '0.0.0.0'
PORT = 51008
SECRET_KEY = 'wesee in hhdt dep dev key'

app = Flask(__name__)
app.config.from_object(__name__)

# load config file
conf_parser = ConfigParser.ConfigParser()
conf_parser.read('config.ini')

WESEE_BASEPATH = conf_parser.get('base', 'path')
db_filename = conf_parser.get('db', 'filename')

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(db_filename)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hi')
def hi():
    c_max_ctime = request.args.get('mc')
    c_tot_count = request.args.get('tc')
    c_cur_album = request.args.get('ca')

    if c_max_ctime is None: return 'hi'
    if c_tot_count is None: return 'hi'
    if c_cur_album is None: return 'hi'
    
    try:
        tc = int(c_tot_count)
        mc = int(c_max_ctime)
        ca = c_cur_album.strip()
    except:
        return 'hi'
    
    db = get_db()
    # compare client max and server max ctime
    rs = db.execute("""
        SELECT album, fn, user, ctime
        FROM photos
        WHERE ctime>?
        AND album=?
    """, [mc, ca]).fetchall()
    # create a return object
    ret = {'count':0, 'photos':[]}
    for r in rs:
        ret['count'] += 1
        ret['photos'].append({
            'a': r[0],
            'f': r[1],
            'u': r[2],
            't': r[3]
        })

    return jsonify(ret)


@app.route('/dl')
def dl():
    c_fn = request.args.get('fn')
    c_ab = request.args.get('ab')

    if c_fn is None: return 'This page does not exist', 404
    if c_ab is None: return 'This page does not exist', 404

    return send_from_directory(os.path.join(WESEE_BASEPATH, c_ab), 
            c_fn, as_attachment=True)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
