from flask import Flask, request, render_template
import pandas as pd
import torch
from transformers import MarianMTModel, MarianTokenizer
from nltk.translate.bleu_score import sentence_bleu
import nltk

app = Flask(__name__)

def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df['english'].tolist(), df['sinhala'].tolist()

english_texts, sinhala_texts = load_dataset("sinhala_english_sentences8.csv")

model_en_to_si = "Helsinki-NLP/opus-mt-en-mul"
model_si_to_en = "Helsinki-NLP/opus-mt-mul-en"

tokenizer_en_to_si = MarianTokenizer.from_pretrained(model_en_to_si)
model_en_to_si = MarianMTModel.from_pretrained(r"C:\Users\User\Downloads\latest_model")
tokenizer_si_to_en = MarianTokenizer.from_pretrained(model_si_to_en)
model_si_to_en = MarianMTModel.from_pretrained(model_si_to_en)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_en_to_si.to(device)
model_si_to_en.to(device)
model_en_to_si.eval()
model_si_to_en.eval()

nltk.download('punkt_tab')

def translate(text, source_lang, target_lang):
    if source_lang == "Sinhala" and target_lang == "English":
        tokenizer = tokenizer_si_to_en
        model = model_si_to_en
    else:
        tokenizer = tokenizer_en_to_si
        model = model_en_to_si

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def calculate_bleu(reference, hypothesis):
    reference_tokens = [nltk.word_tokenize(reference)]
    hypothesis_tokens = nltk.word_tokenize(hypothesis)
    return sentence_bleu(reference_tokens, hypothesis_tokens, weights=(0.25, 0.25, 0.25, 0.25))

def test_translation(input_text, source_lang, target_lang):
    translation = translate(input_text, source_lang, target_lang)
    if source_lang == "English":
        reference = next((sinhala for eng, sinhala in zip(english_texts, sinhala_texts) if eng.lower() == input_text.lower()), translation)
    else:
        reference = next((eng for eng, sinhala in zip(english_texts, sinhala_texts) if sinhala.lower() == input_text.lower()), translation)
    bleu_score = calculate_bleu(reference, translation)
    return {
        'translation': translation
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    source_lang = request.form.get('source_lang', 'English')
    target_lang = request.form.get('target_lang', 'Sinhala')

    if request.method == 'POST':
        input_text = request.form.get('source_text')
        if input_text:
            result = test_translation(input_text, source_lang, target_lang)

    return render_template('index.html', result=result, source_lang=source_lang, target_lang=target_lang)

if __name__ == '__main__':
    app.run(debug=True)