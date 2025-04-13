from flask import Flask, render_template, request, flash, redirect, url_for
from capstone_backend import read_text, translate_text, summarize, pdf_read
import os
import logging


app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = '/home/anmol/Desktop/capstone/Capstone-WebApp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('loginsignup.html')

@app.route('/extract_text', methods=['POST'])
def extract_text():
    file = request.files.get('file')
    if not file or file.filename == '':
        flash('No file selected.')
        return redirect(url_for('home'))
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        if file_ext in ('.jpg', '.jpeg', '.png', '.gif'):
            # Pass the language code dynamically (e.g., 'eng' for English, 'kan' for Kannada)
            language = request.form.get('language', 'eng')  # Default to English
            extracted_text = read_text(file_path, language=language)
            logging.info(f"Processing file: {file_path}")
        elif file_ext == '.pdf':
            extracted_text = pdf_read(file_path)
        else:
            flash('Unsupported file type.')
            return redirect(url_for('home'))
    except Exception as e:
        flash(f'Error processing file: {str(e)}')
        return redirect(url_for('home'))
    finally:
        os.remove(file_path)

    return render_template('extracted_text.html', text=extracted_text)
@app.route('/translate', methods=['POST'])
def translate():
    text = request.form.get('text', '')
    target_lang = request.form.get('target_language', 'en')  # Default to English if not provided
    if not text.strip():
        flash('No text provided for translation.')
        return redirect(url_for('home'))
    
    translated_text = translate_text(text, target_lang)
    return render_template('translated_text.html', text=translated_text)

@app.route('/summarize', methods=['POST'])
def summarize_text():
    text = request.form.get('text', '')
    if not text.strip():
        flash('No text provided for summarization.')
        return redirect(url_for('home'))
    
    summarized_text = summarize(text)
    return render_template('summarized_text.html', text=summarized_text)

if __name__ == '__main__':
    app.run(debug=True)