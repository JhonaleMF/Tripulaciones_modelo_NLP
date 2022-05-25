from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
def signs_texts(text):
            return signos.sub(' ', text.lower())

spanish_stopwords = stopwords.words('spanish')

def remove_stopwords(df):
    return " ".join([word for word in df.split() if word not in spanish_stopwords])

def spanish_stemmer(x):
    stemmer = SnowballStemmer('spanish')
    return " ".join([stemmer.stem(word) for word in x.split()])