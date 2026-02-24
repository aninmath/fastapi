import pickle
import pandas as pd

# import the ml model
# MLFlow
MODEL_VERSION = '1.0.0'

with open('model\\model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict(data: pd.DataFrame):

    prediction = model.predict(data)[0]

    return prediction