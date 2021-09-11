#import para realizar la API
from flask import Flask
#Aqui llegan las peticiones del modelo
from flask import request
#Definiciones que seran usadas en la aplicacion
from flask_restful import Resource, Api, reqparse, abort, marshal, fields

#Imports necesarios para procesar el modelo
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Flatten, Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.applications.vgg16 import VGG16

import io
from PIL import Image
import numpy as np
import base64
import socket

app = Flask("analisis_modelo")
api = Api(app)

model = None

def setModel():
    global model
    new_input = Input(shape=(600, 800, 3))
    base_model = VGG16(include_top=False, input_tensor=new_input)
    flat1 = Flatten()(base_model.layers[-1].output)
    class1 = Dense(1024, activation='relu')(flat1)
    output = Dense(1, activation='sigmoid')(class1)
    model = Model(inputs=base_model.inputs, outputs=output)
    return None

def loadModelWeight():
    global model
    #model.load_weights('/gingivitis/gingivitis.h5')
    opt = SGD(learning_rate=1e-4, momentum=0.9)
    print(model)
    model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
    return None

#API de captura de videos desde el encoder
class analisisAPI(Resource):

    #metodo get
    def get(self):
        #Parametros que son usados en la peticion
        return {'status': True}

    #metodo post
    def post(self):
        #Obtiene los datos de la peticion
        photo = request.form['photo']
        base64_bytes = photo.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        image = np.array(Image.open(io.BytesIO(message_bytes)))
        response = {}
        confidence = model.predict(np.array([image]))[0][0]
        pred = int(round(confidence))
        response['id'] = 1
        response['prediction'] = pred
        response['confidence'] = confidence if pred else 1 - confidence
        return response

#definir ruta de uso de la API
api.add_resource(analisisAPI, "/")

if __name__ == '__main__':
    #seteo de la API en localhost y puerto
    setModel()
    loadModelWeight()
    app.run(host='0.0.0.0', port=5000, debug=True)
