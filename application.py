import nltk
nltk.download('stopwords')
from flask import Flask, jsonify, request
import os
import pickle
import pandas as pd
import re
import numpy as np
from flask_cors import CORS
from utils.config import *
import pymysql


cors = CORS()
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

application = app = Flask(__name__)
cors.init_app(application)


dict_emotions = {

    1: 'Por lo que vemos, te preocupa el proceso de adaptación del acogido. Te recomendamos visitar (Haz clic sobre el botón): <link>',  
    2:'¿Te gustaría contactar con otra familia acogedora para resolver mejor tus dudas?. Dando a continuación clic, podras visitar nuestro Foro: <link>',   
    3: 'No te preocupes si eres soltero y da clic en el siguiente botón para informarte más al respecto: <link>',
    4: 'Si necesitas ayuda para resolver cualquier imprevisto que pueda suceder con el acogido, dando clic al botón accederás a la información que necesitas: <link>',
    5: 'Ayudas económicas. No más dudas! Resuelvelas aquí, primero cliquea el botón: <link>',
    6: 'Es normal que te cuestiones a ti mismo, si tienes lo necesario para brindarle al niño. Por lo tanto, tenemos para tí la siguiente información (Da clic en el botón): <link> ',
    7: 'Te preocupan las despedidas? Muchos han pasado por eso, aquí tienes algunos consejos de como llevarlo lo mejor posible. En el siguiente enlace podrás encontrar toda la información.: <link>'

}
model = pickle.load(open('data/finished_model.pkl','rb'))
emotions_array =np.arange(1, 8)

@application.route('/', methods=['GET'])
def home():
    return """<h1>Desafio Tripulaciones Grupo 3 2020: Modelo detección de emociones de un texto</h1>
                <p>Modelo que detecta la emoción de la respuesta a la pregunta: ¿Cual es tu mayor miedo, duda o inquietud acerca del acogimiento familiar?. Brindando la información que necesita el usuario.</p>
                <p>
                <p>Atacando el endpoint correspondiente podrás acceder al modelo de predicción, o por medio de una plataforma API.</p>
                <h2>Solicitudes API</h2>
                Solicitudes mediante la URL con el siguiente endpoint:
                <p>- Consulta para detectar el grupo de respuesta: URL raíz + /api/v1/consulta?text=Respuesta ingresada</p>
                <p>- Modificar contenido respuestas según tag o clasificación de la respuesta: URL raíz + /api/v1/update?answer=Nueva respuesta&tag=Tag o Categoria del tipo de respuesta</p>
                <p>  </p>
                <p>  Tags o Grupos de respuestas</p>
                <p>  1: Adaptación del niño en la familia.</p>
                <p>  2: Contactar con otra familia acogedora.</p>
                <p>  3: Persona soltera en acoger un niño.</p>
                <p>  4: Ayudas por parte de la asociacón ante cualquier imprevisto.</p>
                <p>  5: Ayudas económicas para una familia acogedora.</p>
                <p>  6: No dar los cuidados suficientes al niño (preocupación a no hacerlo bien).</p>
                <p>  7: Vinculo con el niño.</p>
                

                Plataforma API:
                <p>- Consulta para detectar el grupo de respuesta (GET): Parametro o key "text", con su respectiva respuesta(value). <p>
                <p>- Modificar contenido respuestas según tag o clasificación de la respuesta (PUT): Parametros o keys "answer" y "tag", con su respectivas, nueva respuesta, y tag o grupo de la respuestas(values). <p>"""

@application.route('/api/v1/consulta', methods=["GET"])
def consulta():
    if "text" in request.args:
        def get_answer(prediction):
            query = f'''
            SELECT *
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
            
            cursor.execute(query)
            predict_answer = cursor.fetchall()[0]["respuesta"]
            db.close()
            return predict_answer
        
        signos = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\¿)|(\@)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
        def signs_texts(text):
            return signos.sub(' ', text.lower())

        spanish_stopwords = stopwords.words('spanish')

        def remove_stopwords(df):
            return " ".join([word for word in df.split() if word not in spanish_stopwords])

        def spanish_stemmer(x):
            stemmer = SnowballStemmer('spanish')
            return " ".join([stemmer.stem(word) for word in x.split()])


        consulta = signs_texts(str(request.args["text"]))
        consulta = remove_stopwords(consulta)
        consulta = spanish_stemmer(consulta)
        prediction = model.predict_proba(pd.Series(consulta))[0]
        respond = ""
        for i in emotions_array[prediction > 0.2]:                     
            respond += get_answer(i)
        return jsonify({"respond":respond})
    else:
        return "ERROR : Bad Request"
    
@application.route('/api/v1/update', methods=['PUT'])
def update_question():
    if "answer" in request.args and "tag" in request.args:
        new_answer = request.args['answer']
        tag_answer = int(request.args['tag'])
        def change_answer(new_answer, etiqueta):
            query = f'''
            UPDATE RESPUESTAS
            SET respuesta = '{new_answer}'
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
            #print(query)
            
            cursor.execute(query)
            db.commit()
            db.close()
        change_answer(new_answer, tag_answer)
        return "Successfully changed"
    
    else:
        return "ERROR : Bad Request"
        
    
if __name__ == "__main__":
    application.debug = True
    application.run()