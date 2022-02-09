from nltk.corpus import stopwords
from collections import defaultdict
from nltk.tokenize import word_tokenize
def split_and_clean_words(text: str) -> dict[str, str]:
    """
    Given a document text, return a dictionary of words excluding stopwords
    """
    stop_words = set(stopwords.words('english'))
    wordcount = defaultdict(int)
    BAD_WORDS = ['us', 'let', 'we', 'you','would', 'must']
    for word in word_tokenize(text.lower()):
        word = word.replace('.', '')
        word = word.replace(',' ,'')
        word = word.replace('!' , '')
        word = word.replace('?' , '')
        word = word.replace('-' , '')
        word = word.replace('\'s' , '')
        word = word.replace('\'ve' , '')
        word = word.replace('\'re' , '')
        if word != '':
            if word not in stop_words and word not in BAD_WORDS:
                wordcount[word] += 1
    return wordcount
    
    