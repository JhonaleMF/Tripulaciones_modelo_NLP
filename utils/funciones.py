from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from utils.config import *
from utils.variables import dict_emotions, signos
import pymysql

def signs_texts(text):
            return signos.sub(' ', text.lower())

spanish_stopwords = stopwords.words('spanish')

def remove_stopwords(df):
    return " ".join([word for word in df.split() if word not in spanish_stopwords])

def spanish_stemmer(x):
    stemmer = SnowballStemmer('spanish')
    return " ".join([stemmer.stem(word) for word in x.split()])

def change_answer(new_answer, etiqueta):
    query = f'''
    UPDATE RESPUESTAS
    SET respuesta = {new_answer}'
    WHERE etiqueta = {etiqueta};
    '''
    db = pymysql.connect(host = host,
                        user = username,
                        password = password,
                        cursorclass = pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    
    cursor.connection.commit()
    use_db = '''USE respuestas_openai'''
    cursor.execute(use_db)
    
    cursor.execute(query)
    db.commit()
    db.close()
    
def get_answer(prediction):
    query = f'''
    SELECT respuesta
    FROM RESPUESTAS
    WHERE etiqueta = {prediction};
    '''
    db = pymysql.connect(host = host,
                        user = username,
                        password = password,
                        cursorclass = pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    
    cursor.connection.commit()
    use_db = '''USE respuestas_openai'''
    cursor.execute(use_db)
    
    predict_answer =cursor.execute(query)
    db.close()
    return predict_answer
    