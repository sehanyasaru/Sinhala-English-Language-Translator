# Sinhala-English Translator

A web-based application for real-time translation between Sinhala and English languages, designed to assist language learners and enthusiasts.

## Features

- **Real-time Translation**: Translates text as you type with a 500ms debounce.
- **Language Swapping**: Easily switch between Sinhala and English as source or target languages.
- **Character Counting**: Displays the character count for both source and translated text.
- **Copy Functionality**: Copy translated text to the clipboard with a single click.
- **Example Phrases**: Predefined examples to test the translator.
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices.
- **NLP Integration**: Utilizes machine translation with the MarianMT model and evaluates translation quality using BLEU score.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **NLP**: Transformers library (MarianMT model), NLTK (BLEU score)
- **Dependencies**: PyTorch, pandas

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/sinhala-english-translator.git
   cd sinhala-english-translator
   ```

2. **Install Dependencies**Ensure you have Python 3.8+ installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK Data**Run the following to download required NLTK data:

   ```python
   import nltk
   nltk.download('punkt_tab')
   ```

4. **Prepare the Dataset**

   - Place the `sinhala_english_sentences8.csv` file in the project root directory. The CSV should contain two columns: `english` and `sinhala` with paired sentences.

5. **Set Up Models**

   - Download the pre-trained MarianMT models:
     - English to Sinhala: Use the custom model from `C:\Users\User\Downloads\latest_model` (or adjust the path).
     - Sinhala to English: `Helsinki-NLP/opus-mt-mul-en` (download via Hugging Face).
   - Ensure the model paths are correctly specified in the `app.py` file.

6. **Run the Application**

   ```bash
   python app.py
   ```

   Open your browser and navigate to `http://127.0.0.1:5000/`.

## Project Structure

- `app.py`: Flask backend with translation logic and BLEU score calculation.
- `templates/index.html`: Frontend UI with real-time translation and interactive features.
- `sinhala_english_sentences8.csv`: Dataset of English-Sinhala sentence pairs.
- `requirements.txt`: List of Python dependencies.

## Usage

- Enter text in the source textarea to see real-time translation in the target area.
- Use the swap button to change the source and target languages.
- Click example buttons to insert predefined phrases.
- Clear the input or copy the translated text as needed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss.

## 