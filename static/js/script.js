const sourceText = document.getElementById('source-text');
const sourceCount = document.getElementById('source-count');
const clearTextBtn = document.getElementById('clear-text');
const translatedText = document.getElementById('translated-text');
const translationResult = document.getElementById('translation-result');
const translationPlaceholder = document.getElementById('translation-placeholder');
const loadingIndicator = document.getElementById('loading-indicator');
const copyTextBtn = document.getElementById('copy-text');
const copyTextSpan = copyTextBtn.querySelector('.copy-text');
const copyIcon = copyTextBtn.querySelector('.copy-icon');
const checkIcon = copyTextBtn.querySelector('.check-icon');
const targetCount = document.getElementById('target-count');
const swapLanguagesBtn = document.getElementById('swap-languages');
const sourceLangInput = document.getElementById('source-lang-input');
const targetLangInput = document.getElementById('target-lang-input');
const sourceLangDisplay = document.getElementById('source-lang');
const targetLangDisplay = document.getElementById('target-lang');
const sourceFlag = document.getElementById('source-flag');
const targetFlag = document.getElementById('target-flag');
const translateForm = document.getElementById('translateForm');
const examplesGrid = document.getElementById('examples-grid');

// Debounce function to limit translation requests
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Update character count
function updateCharCount() {
    const count = sourceText.value.length;
    sourceCount.textContent = `${count} characters`;
    clearTextBtn.style.display = count > 0 ? 'flex' : 'none';
}

// Clear source text
function clearSourceText() {
    sourceText.value = '';
    updateCharCount();
    translationResult.textContent = '';
    translationResult.style.display = 'none';
    translationPlaceholder.style.display = 'flex';
    copyTextBtn.style.display = 'none';
    targetCount.textContent = '0 characters';
    translatedText.classList.remove('has-content', 'sinhala-content');
}

// Copy translated text to clipboard
async function copyToClipboard() {
    try {
        await navigator.clipboard.write(translationResult.textContent);
        copyTextBtn.classList.add('copied');
        copyTextSpan.textContent = 'Copied';
        copyIcon.style.display = 'none';
        checkIcon.style.display = 'inline';
        setTimeout(() => {
            copyTextBtn.classList.remove('copied');
            copyTextSpan.textContent = 'Copy';
            copyIcon.style.display = 'inline';
            checkIcon.style.display = 'none';
        }, 2000);
    } catch (err) {
        console.error('Failed to copy text:', err);
    }
}

// Swap languages
function swapLanguages() {
    const tempLang = sourceLangInput.value;
    const tempFlag = sourceFlag.textContent;
    sourceLangInput.value = targetLangInput.value;
    targetLangInput.value = tempLang;
    sourceLangDisplay.textContent = sourceLangInput.value;
    targetLangDisplay.textContent = targetLangInput.value;
    sourceFlag.textContent = targetLangInput.value === 'Sinhala' ? '🇱🇰' : '🇺🇸';
    targetFlag.textContent = sourceLangInput.value === 'Sinhala' ? '🇱🇰' : '🇺🇸';
    sourceText.placeholder = `Enter text in ${sourceLangInput.value}...`;
    clearSourceText();
}

// Handle form submission
async function submitTranslation() {
    if (!sourceText.value.trim()) {
        translationResult.textContent = '';
        translationResult.style.display = 'none';
        translationPlaceholder.style.display = 'flex';
        copyTextBtn.style.display = 'none';
        targetCount.textContent = '0 characters';
        translatedText.classList.remove('has-content', 'sinhala-content');
        return;
    }

    translationPlaceholder.style.display = 'none';
    loadingIndicator.style.display = 'flex';
    translationResult.style.display = 'none';
    copyTextBtn.style.display = 'none';

    const formData = new FormData(translateForm);
    try {
        const response = await fetch('/', {
            method: 'POST',
            body: formData
        });
        const data = await response.text();
        // Parse the response HTML to extract the translation
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, 'text/html');
        const resultElement = doc.querySelector('#translation-result');
        const translation = resultElement ? resultElement.textContent : '';
        translationResult.textContent = translation;
        translationResult.style.display = 'block';
        translationPlaceholder.style.display = 'none';
        loadingIndicator.style.display = 'none';
        copyTextBtn.style.display = 'flex';
        targetCount.textContent = `${translation.length} characters`;
        translatedText.classList.add('has-content');
        if (targetLangInput.value === 'Sinhala') {
            translatedText.classList.add('sinhala-content');
        } else {
            translatedText.classList.remove('sinhala-content');
        }
    } catch (err) {
        console.error('Translation failed:', err);
        translationResult.textContent = 'Error during translation';
        translationResult.style.display = 'block';
        loadingIndicator.style.display = 'none';
    }
}

const debouncedTranslation = debounce(submitTranslation, 500);
function handleExampleClick(event) {
    const btn = event.target.closest('.example-btn');
    if (!btn) return;
    const sourceLang = sourceLangInput.value;
    const text = sourceLang === 'Sinhala' ? btn.dataset.si : btn.dataset.en;
    sourceText.value = text;
    updateCharCount();
    submitTranslation();
}

sourceText.addEventListener('input', () => {
    updateCharCount();
    debouncedTranslation();
});
clearTextBtn.addEventListener('click', clearSourceText);
copyTextBtn.addEventListener('click', copyToClipboard);
swapLanguagesBtn.addEventListener('click', swapLanguages);
translateForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitTranslation();
});
examplesGrid.addEventListener('click', handleExampleClick);

updateCharCount();

