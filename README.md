# GeneratedFrequencyDictionary

A Python NLP tool that generates a frequency dictionary based on the given raw English text. The frequency dictionary can be used for further research (e.g. designing algorithms for text processing, classification, and MT) or linguistic studies (e.g. researching semantics, improving language vocab) 

## Features:
* **Preprocessing** (only "pure" text is analyzed: punctuation and special symbols are left out; multiple newline symbols / invisible characters are reduced for proper tokenization)
* **Tokenization** and **lemmatization** (further text processing is handled by the language model *en_core_web_sm* installed from open-source library spaCy)
* **Absolute** and **relative** frequency for each word form found in text
* **Import** of results to .xlsx format for easy analysis

## Note:
Stop words (such as "a", "the", "is") were **not** removed, since they are crucial for semantics- and syntax-focused tasks

## Installation:
```
pip install -r requirements.txt
```
```
python -m spacy download en_core_web_sm
```
