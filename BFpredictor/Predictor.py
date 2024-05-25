import streamlit as st
import numpy as np
import joblib

# Load the model
model = joblib.load('BFpredictor/bodyfatPredictor.pkl')

st.title('Body Fat Predictor')

# Defining the fields to get the data
weight_unit = st.selectbox('Select weight unit', ['kg', 'lbs'])
weight = st.number_input(f'Weight ({weight_unit})', min_value=0.0, value=70.0)
chest = st.number_input('Chest Circumference (cm)', min_value=0.0, value=90.0)
abdomen = st.number_input('Abdomen Circumference (cm)', min_value=0.0, value=85.0)
hip = st.number_input('Hip Circumference (cm)', min_value=0.0, value=95.0)
thigh = st.number_input('Thigh Circumference (cm)', min_value=0.0, value=55.0)

if weight_unit == 'kg':
    weight = weight / 0.453592 

# Make the prediction when the user click on button
if st.button('Predict Body Fat'):
    input_data = np.array([[weight, chest, abdomen, hip, thigh]])
    body_fat_prediction = model.predict(input_data)
    st.write(f'Estimated Body Fat: {body_fat_prediction[0]:.2f}%')
