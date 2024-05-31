from collections import defaultdict
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


def create_inverted_index(sentences):
    stop_words = set(nltk.corpus.stopwords.words('portuguese'))
    ps = PorterStemmer()

    inverted_index = defaultdict(lambda: defaultdict(int))

    for idx, sentence in enumerate(sentences):
        # Tokenize the sentence
        words = word_tokenize(sentence)

        for word in words:
            # Convert to lower case
            word = word.lower()

            # Remove punctuation and stopwords
            if word.isalnum() and word not in stop_words:
                # Stemming the word
                stemmed_word = ps.stem(word)

                # Update the inverted index
                inverted_index[stemmed_word][idx] += 1

    return inverted_index


