from flask import Flask, jsonify, request
import os
import pickle
import pandas as pd
import re
import numpy as np
from flask_cors import CORS


cors = CORS()
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


application = Flask(__name__)
cors.init_app(application)

dict_emotions = {

    1: 'Por lo que vemos, te preocupa el proceso de adaptación del acogido. Te recomendamos visitar (Haz clic sobre el botón): <link>',  
    2:'¿Te gustaría contactar con otra familia acogedora para resolver mejor tus dudas?. Dando a continuación clic, podras visitar nuestro Foro: <link>',   
    3: 'No te preocupes si eres soltero y da clic en el siguiente botón para informarte más al respecto: <link>',
    4: 'Si necesitas ayuda para resolver cualquier imprevisto que pueda suceder con el acogido, dando clic al botón accederás a la información que necesitas: <link>',
    5: 'Ayudas económicas. No más dudas! Resuelvelas aquí, primero cliquea el botón: <link>',
    6: 'Es normal que tengas miedos. Tenemos para tí la siguiente información (Da clic en el botón): <link> ',
    7: 'No te gustan las despedidas?. Puedes seguir en contacto con el niño sin ningún problema, para más información cliquea el botón: <link>'

}


model = pickle.load(open('data/finished_model.model','rb'))
emotions_array =np.arange(1, 8)

@application.route('/', methods=['GET'])
def home():
    return """<h1>Desafio Tripulaciones Grupo 3 2020: Modelo detección de emociones de un texto</h1>
                <p>Modelo que detecta la emoción de la respuesta a la pregunta: ¿Cual es tu mayor miedo, duda o inquietud acerca del acogimiento familiar?. Brindando la información que necesita el usuario.</p>
                <p>
                <p>Atacando el endpoint correspondiente podrás acceder al modelo de predicción, o por medio de una plataforma API.</p>
                <h2>Solicitudes API</h2>
                Solicitudes mediante la URL con el siguiente endpoint:
                <p>- URL raíz + /api/v1/consulta?text=Respuesta ingresada</p>

                Plataforma API:
                <p>- Parametro o key "text", con su respectiva respuesta(value). <p>"""

@application.route('/api/v1/consulta', methods=["GET"])
def consulta():
    if "text" in request.args:
        signos = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\¿)|(\@)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
        def signs_texts(text):
            return signos.sub(' ', text.lower())

        spanish_stopwords = stopwords.words('spanish')

        def remove_stopwords(df):
            return " ".join([word for word in df.split() if word not in spanish_stopwords])

        def spanish_stemmer(x):
            stemmer = SnowballStemmer('spanish')
            return " ".join([stemmer.stem(word) for word in x.split()])


        consulta = signs_texts(request.args["text"])
        consulta = remove_stopwords(consulta)
        consulta = spanish_stemmer(consulta)
        prediction = model.predict_proba(pd.Series(consulta))[0]
        respond = "Te interesaría la siguiente información:"
        for i in emotions_array[prediction > 0.2]:                        
            respond += " -" + dict_emotions[i]
        return jsonify({"respond":respond})
    
if __name__ == "__main__":
    application.debug = True
    application.run()