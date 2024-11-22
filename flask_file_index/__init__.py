from flask import Flask
import toml
import argparse

app = Flask(__name__)

from flask_file_index import routes
