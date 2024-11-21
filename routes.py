from dl import app
from flask import render_template, abort, send_file
import os


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def index(req_path):

	BASE_DIR = '/home/dl/files'
	abs_path = os.path.join(BASE_DIR, req_path)

	if not os.path.exists(abs_path):
		return abort(404)

	if os.path.isfile(abs_path):
		return send_file(abs_path)

	files = os.listdir(abs_path)

	return render_template('index.html', directory=req_path, files=files)
