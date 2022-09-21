from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "first keep it safe"

bcrypt = Bcrypt(app)