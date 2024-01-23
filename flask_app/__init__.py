from flask import Flask, flash
app = Flask(__name__)
app.secret_key = "It is a secret"

DATABASE = "login_and_registration_schema"
