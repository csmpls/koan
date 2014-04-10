from flask import Flask, render_template, request, redirect, url_for, jsonify, g
from sqlite3 import dbapi2 as sqlite3
import json, os

app = Flask(__name__)


# ----------------------- db shit

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'koan.db'),
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

# --------------------------- queries

def get_random_post():
    db = get_db()
    rand = db.execute('select text, id from posts order by RANDOM() limit 1')
    post = rand.fetchone()

    if post is None:
        post = ("no posts yet :B",0)

    return post

def get_newest_post():
    db = get_db()

    cur = db.execute('select text from posts order by id desc')
    posts = cur.fetchone()

    if not posts:
        post = "no posts yet :B"

    return post

def add_post(post):
    db = get_db()
    db.execute('insert into posts (text) values (?)', [post])
    db.commit()

def delete_post(id):
    db = get_db()
    db.execute('delete from posts where id = '+id)
    db.commit()







# ---------------------------- routes

@app.route('/')
@app.route('/index')
def index():

    post = get_random_post() 

    return render_template("index.html", post=post[0], id=post[1])


@app.route('/get', methods=['GET'])
def get():

    post = get_random_post() 

    return render_template("index.html", post=post[0], id=post[1])
	

@app.route('/post', methods=['POST'])
def post():

    post = request.json['payload']

    add_post(post)

    post = get_random_post() 

    print(post)


    return jsonify(status="ok", post=post[0], id=post[1])


@app.route('/delete', methods=['POST'])
def delete():

    id = request.json['payload']

    delete_post(id)

    post = get_random_post() 

    return jsonify(status="ok", post=post[0], id=post[1])








if __name__ == '__main__':
    init_db()
    app.run()