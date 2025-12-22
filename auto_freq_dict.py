import re
import pandas as pd
import spacy
from spacy.tokens import Doc

nlp = spacy.load("en_core_web_sm")


def preprocessing(input_text):
    input_text = str(input_text)
    input_text = re.sub(r"\b[A-Z]\.", " ", input_text)
    input_text = input_text.lower()
    input_text = re.sub(r"[’ʼ`]", "'", input_text)
    input_text = re.sub(r"\d+", "", input_text)
    input_text = re.sub(r"[^a-z'\-\s]", " ", input_text)
    input_text = re.sub(r"\s-\s", " ", input_text)
    input_text = re.sub(r"\s+", " ", input_text).strip()
    return input_text


num_of_samples = False      # int or False
tokens_per_sample = 1000    # int


def generate_freq_dict(input_text):
    with open(input_text, "r+", encoding="utf-8") as f:
        text = f.read()

    cleaned_text = preprocessing(text)

    text_tokens = cleaned_text.split()

    print(f"\nTotal amount of tokens after preprocessing: {len(text_tokens)}")

    if num_of_samples:
        final_samples = num_of_samples

    else:
        final_samples = len(text_tokens) // tokens_per_sample
        print(f"\nAmount of samples was not pre-defined. Found enough tokens for {final_samples} samples.")

    print(f"\nDividing into {final_samples} samples by {tokens_per_sample} tokens:")

    data_registry = {}

    for i in range(final_samples):
        start_index = i * tokens_per_sample
        end_index = start_index + tokens_per_sample

        if end_index > len(text_tokens):
            print(f"Warning! Text ended on sample №{i + 1}. Not enough words.")
            break

        sample_tokens = text_tokens[start_index: end_index]

        doc = Doc(nlp.vocab, words=sample_tokens)
        doc = nlp(doc)

        for token in doc:
            word_form = token.text
            lemma = token.lemma_
            pos_tag = token.pos_

            corrections = {
                # "<word_form>": ("<lemma>", "<pos_tag>"),
            }

            if word_form in corrections:
                lemma, pos_tag = corrections[word_form]

            key = (word_form, lemma, pos_tag)

            if key not in data_registry:
                data_registry[key] = [0] * final_samples

            data_registry[key][i] += 1

        print(f"Processed sample {i + 1}/{final_samples}")

    rows = []
    for (word_form, lemma, pos), freqs in data_registry.items():
        total_freq = sum(freqs)
        row = [word_form, lemma, pos, total_freq] + freqs
        rows.append(row)

    freq_cols = [f"freq{i + 1}" for i in range(final_samples)]
    columns = ["word_form", "lemma", "pos", "freq"] + freq_cols

    df = pd.DataFrame(rows, columns=columns)

    df = df.sort_values(by="freq", ascending=False).reset_index(drop=True)

    df.insert(0, "id", df.index + 1)

    df.to_excel("frequency_dictionary_eng.xlsx", index=False)

    return print("\nDictionary successfully created. Results saved in \"frequency_dictionary_eng.xlsx\"")


generate_freq_dict("the-picture-of-dorian-gray-X-chapters-en.txt")
