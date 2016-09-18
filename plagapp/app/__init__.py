from flask import Flask

app = Flask(__name__)

# Load config variables (notably PLAGCOMPS_LOC)
app.config.from_object('config')

from app import routes