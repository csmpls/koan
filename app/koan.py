from flask import Flask, render_template, request, redirect, url_for, jsonify, g
from sqlite3 import dbapi2 as sqlite3
import json, os

app = Flask(__name__)










# ----------------------- db shit

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('KOAN_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


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





# --------------------------- helpers

def get_newest_post():
    db = get_db()

    cur = db.execute('select text from posts order by id desc')
    posts = cur.fetchall()
    try:
        post = posts[0]
    except:
        post = "no posts yet :B"

    return post






# ---------------------------- routes

@app.route('/')
@app.route('/index')
def index():

    post = get_newest_post() 

    return render_template("index.html", post=post)
	

@app.route('/post', methods=['POST'])
def post():

	post = request.json['submission']

	db = get_db()
	db.execute('insert into posts (text) values (?)', 
		[post])
	db.commit()

	return jsonify(status="ok", post=post)


@app.route('/get', methods=['GET'])
def get():

    post = get_newest_post()

    return jsonify(post=post['text'])

if __name__ == '__main__':
    init_db()
    app.run(host='128.32.226.246', port=4217)
