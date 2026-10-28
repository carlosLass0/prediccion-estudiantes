import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="API de Predicción de Rendimiento Académico")

try:
    model = joblib.load('mlp_model.pkl')
    scaler = joblib.load('scaler.pkl')
except Exception as e:
    print(f"Error al cargar los modelos: {e}")

class StudentData(BaseModel):
    Tareas: float
    Examenes: float
    Asistencia: float
    Estudio_Horas: float
    Sueno_Horas: float
    Extracurriculares: int

@app.get("/")
def home():
    return {"status": "running", "message": "API de Predicción Académica Activa"}

@app.post("/predict")
def predict(data: StudentData):
    try:
        features = np.array([[
            data.Tareas,
            data.Examenes,
            data.Asistencia,
            data.Estudio_Horas,
            data.Sueno_Horas,
            data.Extracurriculares
        ]])
        features_scaled = scaler.transform(features)
        prediction = int(model.predict(features_scaled)[0])
        probabilities = model.predict_proba(features_scaled)[0]
        prob_aprobacion = float(probabilities[1])
        estado = "Aprobado" if prediction == 1 else "Reprobado"
        return {
            "aprobado": prediction,
            "estado": estado,
            "probabilidad_aprobacion": prob_aprobacion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
