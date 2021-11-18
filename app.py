from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from predict import predict

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        filename = request.files['file']
        filename = secure_filename(filename.filename)

        filepath = 'test/' + filename
        # print(filename)
        description = predict(filepath)
        output = {
            "filename": filename,
            "description": description
        }
        return render_template('result.html', result=output)
    return None


if __name__ == '__main__':
    app.run(debug=True)
