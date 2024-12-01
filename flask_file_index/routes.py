from flask_file_index import app
from flask import render_template, abort, send_file
import os
import mimetypes
import datetime
import markdown

ICONS = {
	'text/x-python': 'filetype-py',
}

def human_readable_size(size):
	for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
		if size < 1024.0:
			return f'{size:.2f} {unit}'
		size /= 1024.0


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def index(req_path):

	base_dir = os.environ.get('FFI_BASE_DIR', '.')
	abs_path = os.path.abspath(os.path.join(base_dir, req_path))

	if not os.path.exists(abs_path):
		return abort(404)

	if os.path.isfile(abs_path):
		return send_file(abs_path)

	readme = ''
	if os.path.exists(os.path.join(abs_path, 'README.md')):
		readme = markdown.markdown(open(os.path.join(abs_path, 'README.md'), 'r').read())

	files = []
	for f in os.listdir(abs_path):
		if f == 'README.md':
			continue;

		abs_file_path = os.path.join(abs_path, f)
		mime_type = mimetypes.guess_type(abs_file_path)[0]

		files.append({
			'filename': f,
			'isdir': os.path.isdir(abs_file_path),
			'type': mime_type,
			'mtime': datetime.datetime.fromtimestamp(os.path.getmtime(abs_file_path)).replace(second=0, microsecond=0).isoformat(),
			'icon': ICONS.get(mime_type, 'question'),
			'size': human_readable_size(os.path.getsize(abs_file_path)),
		})

	files = sorted(files, key=lambda x: x['filename'])
	files = sorted(files, key=lambda x: x['isdir'], reverse=True)

	return render_template('index.html', directory=req_path.replace('/', ' / '), files=files, up=os.path.dirname(req_path), readme=readme)
