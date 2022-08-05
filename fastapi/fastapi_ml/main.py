from fastapi import FastAPI
import pickle
import numpy as np
import pandas as pd
import os

from models import IrisSpecies


app = FastAPI()

@app.get('/')
async def app_index():
    return {
       'response_code': 200,
       'text': 'welcome to the root of this simple Machine Learning app',
       'available routes' : '/predict, expects 4 numerical values as params',
       'documentation' : '/docs'
        }

@app.post('/predict')
async def predict_species(iris: IrisSpecies):
    data = iris.dict()
    model_path = os.path.join('ml_model','LRClassifier.pkl')
    loaded_model = pickle.load(open(model_path, 'rb'))
    data_in = [[data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']]]
    prediction = loaded_model.predict(data_in)
    probability = loaded_model.predict_proba(data_in).max()
    return {
       'response_code': 200,
       'prediction': prediction[0],
       'probability': probability
        }



