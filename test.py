import os
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from flask import send_from_directory
import random
import pyvips
import io

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MIME_TYPES={'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','gif':'image/gif'}
print(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        ext="png"
        if request.form.get("ext") in ALLOWED_EXTENSIONS:
            ext=request.form.get("ext")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename,ext=ext))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file"/>
      <input type="text" name="ext" value="png"/>
      <input type="submit" value="Upload"/>
    </form>
    '''

@app.route('/uploads/<filename>/<ext>')
def uploaded_file(filename, ext):
        try:
            if ext not in ALLOWED_EXTENSIONS:
                ext='png'
            new_image = pyvips.Image.thumbnail(os.path.join(app.config['UPLOAD_FOLDER'],filename), 400, height=400)
            new_filename = os.path.join(app.config['UPLOAD_FOLDER'],'thumb%s.%s' % (filename.split('.')[0], ext))
            new_image.write_to_file(new_filename)
            return send_file(new_filename, mimetype=MIME_TYPES[ext])
        except Exception as e:
            return '''
            <!doctype html>
            <h1>Invalid picture</h1>
            '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8085)
