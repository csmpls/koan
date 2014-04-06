#!bin/python
from app import app

SECRET_KEY = 'a666ccceeeffff'
app.secret_key = SECRET_KEY
app.run(debug = True)
