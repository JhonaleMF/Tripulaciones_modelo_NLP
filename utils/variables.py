import numpy as np
import pickle
import re

home = """<h1>Desafio Tripulaciones Grupo 3 2020: Modelo detección de emociones de un texto</h1>
                <p>Modelo que detecta la emoción de la respuesta a la pregunta: ¿Cual es tu mayor miedo, duda o inquietud acerca del acogimiento familiar?. Brindando la información que necesita el usuario.</p>
                <p>
                <p>Atacando el endpoint correspondiente podrás acceder al modelo de predicción, o por medio de una plataforma API.</p>
                <h2>Solicitudes API</h2>
                Solicitudes mediante la URL con el siguiente endpoint:
                <p>- URL raíz + /api/v1/consulta?text=Respuesta ingresada</p>

                Plataforma API:
                <p>- Parametro o key "text", con su respectiva respuesta(value). <p>"""
                
dict_emotions = {

    1: 'Por lo que vemos, te preocupa el proceso de adaptación del acogido. Te recomendamos visitar (Haz clic sobre el botón): <link>',  
    2:'¿Te gustaría contactar con otra familia acogedora para resolver mejor tus dudas?. Dando a continuación clic, podras visitar nuestro Foro: <link>',   
    3: 'No te preocupes si eres soltero y da clic en el siguiente botón para informarte más al respecto: <link>',
    4: 'Si necesitas ayuda para resolver cualquier imprevisto que pueda suceder con el acogido, dando clic al botón accederás a la información que necesitas: <link>',
    5: 'Ayudas económicas. No más dudas! Resuelvelas aquí, primero cliquea el botón: <link>',
    6: 'Es normal que te cuestiones a ti mismo, si tienes lo necesario para brindarle al niño. Por lo tanto, tenemos para tí la siguiente información (Da clic en el botón): <link> ',
    7: 'Te preocupan las despedidas? Muchos han pasado por eso, aquí tienes algunos consejos de como llevarlo lo mejor posible. En el siguiente enlace podrás encontrar toda la información.: <link>'

}
signos = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\¿)|(\@)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
model = pickle.load(open('data/finished_model.pkl','rb'))
emotions_array =np.arange(1, 8)

respond = "Te interesaría la siguiente información:"