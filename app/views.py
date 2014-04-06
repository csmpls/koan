from flask import render_template, request, redirect, url_for, jsonify
import json
from app import app

# index controls (1) login (2) post display
@app.route('/')
@app.route('/index')
def index():

	#post = get()

	post = "hi lol"

	return render_template("index.html", post=post)
	
@app.route('/post', methods=['POST'])
def post():

	post = request.json

	print(post)

	return jsonify(status="ok")
