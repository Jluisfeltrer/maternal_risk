import streamlit as st
import joblib
import pandas as pd
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.preprocessing import crear_indicador_fiebre

modelo = joblib.load(os.path.join(BASE_DIR, 'models' 'model.pkl'))


st.title('Prediccion de riesgo materno')
st.write('Introduce los signos vitales de la paciente para estimar su nivel de riesgo durante el embarazo')


st.header('Datos de la paciente')

age = st.slider('Edad (años)', min_value=10, max_value=70, value=25)
systolic_bp = st.slider('Presion arterial sistolica (mmHg)', min_value=70, max_value=160, value=120)
diastolic_bp = st.slider('Presion arterial diastolica (mmHg)', min_value=49, max_value=100, value=80)
bs = st.slider('Glucosa en sangre (mmol/L)', min_value=6.0, max_value=19.0, value=7.5, step=0.1)
heart_rate = st.slider('Frecuencia cardiaca (bpm)', min_value=50, max_value=90, value=75)
body_temp_c = st.slider('Temperatura corporal (C)', min_value=36.0, max_value=40.0, value=36.7, step=0.1)


df_input = pd.DataFrame({
    'BodyTemp' : [body_temp_c]
})
df_input = crear_indicador_fiebre(df_input)

datos_paciente = pd.DataFrame({
    'Age': [age],
    'SystolicBP': [systolic_bp],
    'DiastolicBP': [diastolic_bp],
    'BS': [bs],
    'HeartRate': [heart_rate],
    'tiene_fiebre': [df_input['tiene_fiebre'].iloc[0]]
})

if st.button('Predecir el nivel de riesgo'):
    prediccion = modelo.predict(datos_paciente)[0]
    st.subheader(f'Nivelde riesgo estimado: {prediccion}')
