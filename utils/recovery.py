import json
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


def load_inverted_index(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def search_inverted_index(query, inverted_index):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    query_tokens = word_tokenize(query.lower())
    query_terms = [ps.stem(word) for word in query_tokens if word.isalnum() and word not in stop_words]

    results = defaultdict(int)

    for term in query_terms:
        if term in inverted_index:
            for doc_id, freq in inverted_index[term].items():
                results[int(doc_id)] += freq  # Garantir que doc_id é int

    ranked_results = sorted(results.items(), key=lambda item: item[1], reverse=True)

    return ranked_results


def display_results(ranked_results, documents):
    for doc_id, score in ranked_results:
        if 0 <= doc_id < len(documents):
            print(
                f"Documento {doc_id} - Nome: {documents[doc_id]['nome']} - URL: {documents[doc_id]['url']} - Score: {score}")
