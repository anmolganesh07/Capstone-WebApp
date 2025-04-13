


from flask import Flask, render_template, request
from capstone_backend import read_text, translate_text, summarize, pdf_read
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('loginsignup.html')

@app.route('/extract_text', methods=['GET', 'POST'])
def extract_text():
    if request.method == 'POST':
        file = request.files['file']
        language=request.form['language']
        file_ext = os.path.splitext(file)[1]
        if file_ext in ('.jpg', '.jpeg', '.png', '.gif'):
            extracted_text = read_text(file)
        elif file_ext == '.pdf':
            extracted_text = pdf_read(file)
        return render_template('extracted_text.html', text=extracted_text)
    return render_template('extract_text.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        extracted_text = request.form['text']
        translated_text = translate_text(extracted_text)
        return render_template('translated_text.html', text=translated_text)
    return render_template('translate.html')

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'POST':
        extracted_text = request.form['text']
        summarized_text = summarize(extracted_text, 40)
        return render_template('summarized_text.html', text=summarized_text)
    return render_template('summarize.html')

if __name__ == '__main__':
    app.run(debug=True)
