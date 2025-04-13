import nltk
from googletrans import Translator
import pytesseract
from easyocr import Reader
import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
import logging
from PIL import Image, ImageEnhance


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

nltk.download("stopwords")
nltk.download("punkt")


# def preprocess_image(image_path):
#     """Preprocess the image to improve OCR accuracy."""
#     image = Image.open(image_path)
#     image = image.convert("L")  # Convert to grayscale
#     enhancer = ImageEnhance.Contrast(image)
#     image = enhancer.enhance(2)  # Increase contrast
#     preprocessed_path = image_path.replace(".jpg", "_preprocessed.jpg")
#     image.save(preprocessed_path, resample=Image.Resampling.LANCZOS)  # Use LANCZOS for resampling
#     return preprocessed_path

# Initialize OCR models
reader_general = Reader(["en", "hi"])
reader_kannada = Reader(["kn", "en"])  # Kannada with English
reader_chinese = Reader(["ch_sim", "en"])
reader_arabic = Reader(["ar", "en"])

def read_text(image_path, language="en"):
    """Extract text from an image using OCR."""
    try:
        # List of supported languages
        supported_languages = ["en", "hi", "kn", "ar", "ch_sim"]

        # Check if the language is supported
        if language not in supported_languages:
            logging.error(f"Unsupported language: {language}")
            return f"Error: Unsupported language '{language}'. Supported languages are: {', '.join(supported_languages)}."

        # Preprocess the image
        # preprocessed_path = preprocess_image(image_path)

        # Select the appropriate OCR reader
        if language == 'kn':
            text = reader_kannada.readtext(image_path, detail=0, paragraph=False)
        elif language == 'ar':
            text = reader_arabic.readtext(image_path, detail=0, paragraph=False)
        elif language == 'ch_sim':
            text = reader_chinese.readtext(image_path, detail=0, paragraph=False)
        else:
            text = reader_general.readtext(image_path, detail=0, paragraph=False)

        return '\n'.join(text)
    except Exception as e:
        logging.error(f"Error reading text from image: {str(e)}")
        return "Error: Unable to process the image."

def pdf_read(pdf_path):
    """Extract text from a PDF."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        logging.error(f"Error reading PDF: {str(e)}")
        return ""

def translate_text(text, target_lang):
    """Translate text to the target language."""
    try:
        translator = Translator()
        # Automatically detect the source language
        detected_lang = translator.detect(text).lang
        logging.info(f"Detected source language: {detected_lang}")
        
        # Translate the text
        translated_text = translator.translate(text, src=detected_lang, dest=target_lang)
        return translated_text.text
    except Exception as e:
        logging.error(f"Error during translation: {str(e)}")
        return ""

def summarize(text):
    """Summarize the given text."""
    try:
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        words = [word for word in words if word.lower() not in stop_words]
        freq = nltk.FreqDist(words)
        scores = {}
        for i, sentence in enumerate(sentences):
            for word in word_tokenize(sentence.lower()):
                if word in freq:
                    scores[i] = scores.get(i, 0) + freq[word]
        top_sentences = nlargest(5, scores, key=scores.get)
        summary = " ".join([sentences[i] for i in sorted(top_sentences)])
        return summary
    except Exception as e:
        logging.error(f"Error during summarization: {str(e)}")
        return ""