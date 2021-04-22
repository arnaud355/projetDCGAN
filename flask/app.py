from flask import Flask,render_template,url_for, redirect,request,send_file, Response,send_from_directory,json
#from flask_json import FlaskJSON, JsonError, json_response
import pandas as pd
import keras
import numpy as np
import pickle
from keras.models import load_model
from numpy.random import randn
from keras.models import model_from_json
from keras.models import model_from_yaml
from pymongo import MongoClient
import yaml
import json
from yaml import load, dump
import pandas as pd
import re
from bson.json_util import dumps
import matplotlib as plt
from matplotlib import pyplot
#import json
import time
import pymongo
import h5py
import os
import sentry_sdk
import glob
import gridfs
import io
import base64
import PIL.Image as Image
from array import array
from bson import Regex

from sentry_sdk.integrations.flask import FlaskIntegration
#activate cifar, cd Desktop\dataIA\projetFilRouge\E1_projetFilRougeDl\flask  : python app.py
app = Flask(__name__)
#json = FlaskJSON(app)
#api = Api(app)  # type: Api
app.config['UPLOAD_FOLDER'] = 'static/result'
app.config['DATA_DIR'] = '/Users/arnaud.baleh/Desktop/dataIA/projetFilRouge/E1_projetFilRougeDl/flask/static/'

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0
)

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0
    
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route("/")
def accueil_page():
  
    files = glob.glob('static/tmp/*.png', recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
             
    return render_template("accueil.html")

@app.route("/handleTheme", methods=['POST'])
def handleThemePicture():
    valeur = request.form['themeChoix']
    
    # generate points in latent space as input for the generator
    def generate_latent_points(latent_dim, n_samples):
        # generate points in the latent space
        x_input = randn(latent_dim * n_samples)
        # reshape into a batch of inputs for the network
        x_input = x_input.reshape(n_samples, latent_dim)
        return x_input

    # plot the generated images
    def create_plot(examples, n):
        # plot images
        for i in range(n * n):
            # define subplot
            pyplot.subplot(n, n, 1 + i)
            # turn off axis
            pyplot.axis('off')
            # plot raw pixel data
            pyplot.imshow(examples[i, :, :])
        #pyplot.show()
        plt.pyplot.imsave("/Users/arnaud.baleh/Desktop/dataIA/projetFilRouge/E1_projetFilRougeDl/flask/static/result/imageFantasy.png",examples[n])
    
    debut = time.time()
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["datasetChefOeuvre"]
    mycol = mydb["model"]
    cursor = mycol.find()
    myWeightsCol = mydb["weightsStorage"]
    
    json_data = ()
    for document in cursor:
        json_data = document
    
    json_data = str(json_data)
    json_data = re.sub('\'', '"', json_data)
    pattern = '"_id": ObjectId\(\"[a-zA-Z0-9_]{24}\"\),\s'
    json_data = re.sub(pattern, '', json_data)
    json_data = re.sub("None", 'null', json_data)
    json_data = re.sub("False", 'false', json_data)
    json_data = re.sub("True", 'true', json_data)
    file = open("static/modelDCGAN.json", "w")
    file.write(json_data)
    file.close()    
    
    # load Json and create model
    json_file = open('static/modelDCGAN.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    
    if valeur == "cartoon":
        
        #Load of weights
        #loaded_model.load_weights(myWeightsCol.find({'weightsCartoon':'C:/Users/arnaud.baleh/Desktop/dataIA/projetFilRouge/E1_projetFilRougeDl/flask/modelWeightsCartoon.h5'}))
        myArray = []
        mydoc = myWeightsCol.find({'url':{'$regex':'Cartoon'}})
        
        for x in mydoc:
            myArray.append(str(x))
            
        myString = str(myArray)
        url = re.findall(r"C:/Users/arnaud.baleh/Desktop/dataIA/projetFilRouge/E1_projetFilRougeDl/flask/[a-zA-Z0-9]{10,50}.h5", myString)
        url = str(url)
        url = url[2:]
        url = url[:-2]
        loaded_model.load_weights(url)
        
    elif valeur == "videogaming":
        myArray = []
        mydoc = myWeightsCol.find({'url':{'$regex':'VideoGamingCharacters'}})
        
        for x in mydoc:
            myArray.append(str(x))
            
        myString = str(myArray)
        url = re.findall(r"C:/Users/arnaud.baleh/Desktop/dataIA/projetFilRouge/E1_projetFilRougeDl/flask/[a-zA-Z0-9]{10,50}.h5", myString)
        url = str(url)
        url = url[2:]
        url = url[:-2]
        loaded_model.load_weights(url)
    
    elif valeur == "heroic-fantasy":
        myArray = []
        mydoc = myWeightsCol.find({'url':{'$regex':'heroicFantasy'}})
        
        for x in mydoc:
            myArray.append(str(x))
            
        myString = str(myArray)
        url = re.findall(r"C:/Users/arnaud.baleh/Desktop/dataIA/projetFilRouge/E1_projetFilRougeDl/flask/[a-zA-Z0-9]{10,50}.h5", myString)
        url = str(url)
        url = url[2:]
        url = url[:-2]
        loaded_model.load_weights(url)
    
    elif valeur == "heroes":
        myArray = []
        mydoc = myWeightsCol.find({'url':{'$regex':'Superheroes'}})
        
        for x in mydoc:
            myArray.append(str(x))
            
        myString = str(myArray)
        url = re.findall(r"C:/Users/arnaud.baleh/Desktop/dataIA/projetFilRouge/E1_projetFilRougeDl/flask/[a-zA-Z0-9]{10,50}.h5", myString)
        url = str(url)
        url = url[2:]
        url = url[:-2]
        loaded_model.load_weights(url)
    
    elif valeur == "saga":
        myArray = []
        mydoc = myWeightsCol.find({'url':{'$regex':'SagaIntergalactique'}})
        
        for x in mydoc:
            myArray.append(str(x))
            
        myString = str(myArray)
        url = re.findall(r"C:/Users/arnaud.baleh/Desktop/dataIA/projetFilRouge/E1_projetFilRougeDl/flask/[a-zA-Z0-9]{10,50}.h5", myString)
        url = str(url)
        url = url[2:]
        url = url[:-2]
        loaded_model.load_weights(url)
    
    elif valeur == "":
        return "<h3>Vous n'avez pas sélectionné de thème!</h3>"
    else:
        text = "Thème " + valeur + " pas encore disponible"
        return render_template("rendu.html",text=text,x=valeur)
        
    # generate images
    latent_points = generate_latent_points(100, 100)
    # generate images
    #X = model.predict(latent_points)
    X = loaded_model.predict(latent_points)
    # scale from [-1,1] to [0,1]
    X = (X + 1) / 2.0
    # plot the result
    create_plot(X, 1)
    
    fin = time.time()
    temps = fin - debut
    #return render_template("rendu.html",value=temps)
    temps = str(temps)
    file = open("temps.txt", "w")
    file.write(temps)
    file.close()
    
    valeur = str(valeur)
    file = open("choix.txt", "w")
    file.write(valeur)
    file.close()

    return redirect(url_for('view_picture'))

@app.route("/get_result")
def view_picture():

    imgs = []
    path = 'static/result/'
    for f in os.listdir(path):
        imgs.append(f)

    taille = len(imgs) - 1
    picture = imgs[taille]
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], picture)
    
    file = open("temps.txt", "r")
    temps = file.read()
    file.close()
    
    file = open("choix.txt", "r")
    choix = file.read()
    file.close()

    return render_template("rendu.html", image_color=full_filename,value=temps,choix=choix)

#@route('/images/<filename>')
@app.route("/handleImage", methods=['POST'])
#def image(filename):
def image():
    choix = request.form['choix']
    nombre = request.form['nombre']
    
    if choix == "":
        choix = "file"
        
    if nombre == "":
        nombre = 5
    
    nombre = int(nombre)
    array = []
    v = 0
    for i in range(1,nombre + 1):
        v = v + 1
        w = v
        w = str(w)
        array.append(choix + w)
 
        
    #array = ["VideoGamingCharacters146","VideoGamingCharacters147","VideoGamingCharacters148","VideoGamingCharacters149","VideoGamingCharacters150"] 
    # connect to database
    connection = pymongo.MongoClient("mongodb://localhost:27017/")
    db = connection['DbDatasets']
    fs = gridfs.GridFS(db)
    
    #filename = "VideoGamingCharacters146"
    #gridout = fs.get_last_version(filename=filename)
    
    path = 'static/tmp/'
    for ele in array:
        data = fs.get_last_version(ele).read()
        image = Image.open(io.BytesIO(data))
        image.save(path + ele + ".png", "PNG")
   
    #response.content_type = 'image/png'
    #return gridout
  

    return render_template("displayDataset.html",nb=nombre,tab=array)
    
if __name__ == "__main__":
    app.run(debug=True)