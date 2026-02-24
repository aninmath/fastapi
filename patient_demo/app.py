from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
app = FastAPI()
from patient import Patient, Patientupdate


def load_data():
    with open ('data.json','r') as f:
        data = json.load(f)
        return data

def write_data(data:dict):
    with open ('data.json', 'w+') as f:
        json.dump(data,f)


@app.get('/')

def hello():
    return {'message': 'hello world'}


@app.get('/about')

def about():
    return {'message': 'this is about'}


@app.get('/view')

def view():
    data = load_data()
    return data



@app.get('/patient/{id}')

def view_patient(id:str = Path(...,description= 'id of the patient', example= 'P001')):
    data = load_data()

    if id in data:
        return data[id]
    raise HTTPException(status_code=404, detail= 'Patient not found')


@app.get('/sort')

def sort_patient(field:str = Query(...,description='sort on basis of BMI, height or weight'), 
                 order : str = Query('asc', description= 'sort by asc or desc')):
    
    field = field.lower()
    order = order.lower()
    
    valid_fields = ['height', 'weight', 'bmi']

    if field not in valid_fields:
        raise HTTPException (status_code= 400, detail= f'not selected from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException (status_code= 400, detail= 'invalid order')
    

    data = load_data()

    data_sorted = sorted(data.items(), key = lambda x: x[1][field], reverse = (order == 'desc')) 

    return data_sorted



@app.post('/create')

def create_patient(record : Patient):
    data = load_data()

    if record.id in data:
        raise HTTPException (status_code= 404, detail= 'patient already available')
    
    data[record.id] = record.model_dump(exclude=['id'])

    write_data(data)

    return JSONResponse(status_code=201, content={'message':f'patient with id {record.id} created successfully'})



@app.put('/edit/{id}')

def update_patient(id:str , Updaterecord : Patientupdate):

    data = load_data()

    if id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    existing_patient_info = data[id]

    updated_info = Updaterecord.model_dump(exclude_unset= True)

    for key, value in updated_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = id

    Patient_pydantic = Patient(**existing_patient_info)

    existing_patient_info = Patient_pydantic.model_dump(exclude='id')

    data[id] = existing_patient_info

    write_data(data)

    return JSONResponse(status_code= 200, content= {'message': f"patient id {id} successfully edited"})



@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    write_data(data)

    return JSONResponse(status_code=200, content={'message':f'patient {patient_id} deleted'})