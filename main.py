from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from schema.insurance import InsuranceInput
from src.prediction import predict, model, MODEL_VERSION




app = FastAPI()

# human readable       
@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction API'}

# machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }


@app.post("/predict")
def predict_premium(data: InsuranceInput):

    input_df = pd.DataFrame([{
        "age": data.age,
        "sex": data.sex,
        "bmi": data.bmi,
        "children": data.children,
        "smoker": data.smoker,
        "region": data.region
    }])

    try:

        prediction = round(float(predict(input_df)), 2)

        return JSONResponse(
            status_code=200,
            content={"predicted_charges": prediction}
        )
    except Exception as e:

        return JSONResponse(status_code=500, content={"error": str(e)})