import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask.helpers import flash
from werkzeug.utils import secure_filename

from predict import predict

app = Flask(__name__)


UPLOAD_FOLDER = '/'
ALLOWED_EXT = set(['png', 'jpg', 'jpeg', 'bmp'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(filename)
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )


@app.route('/predict', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')

        file = request.files['file']
        if file.filename == '':
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        filepath = url_for('uploaded_file', filename=filename)
        # filepath = f'http://0.0.0.0:{PORT}{filepath}'
        filepath = f'http://localhost:{PORT}{filepath}'
        print('\n', filepath, '\n')

        description = predict(filepath)
        description = description[6:-4]

        output = {
            "filename": filename,
            "description": description
        }

        return render_template('result.html', result=output)
    # return redirect(/)


# @app.route('/predict', methods=['GET', 'POST'])
# def result():
#     if request.method == 'POST':
#         filename = request.files['file']
#         filename = secure_filename(filename.filename)

#         filepath = 'static/images/' + filename
#         # print(filename)

#         description = predict(filepath)
#         description = description[6:-4]

#         output = {
#             "filename": filename,
#             "description": description
#         }
#         return render_template('result.html', result=output)
#     return None


if __name__ == '__main__':
    PORT = 5000
    # Only for production
    # app.run(host='0.0.0.0')
    app.run(host='localhost')
