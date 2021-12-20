import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
import pickle

def main():
    st.title("Emotion recognition evaluation")

    st.sidebar.title("Settings")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Main page", "Real-time evaluation simulation", "Models overview"])

    if app_mode == "Show instructions":
        st.sidebar.success('Next, try selecting "Real-time evaluation simulation".')

    elif app_mode == "Real-time evaluation simulation":
        eval()

    elif app_mode == "Models overview":
        models()

    return None


def eval():
    st.subheader("Real-time evaluation simulation")

    model_selection = st.selectbox('Select model', {'Random Forest', 'LightGBM'})

    if model_selection == 'Random Forest' :
        model = pickle.load(open("Models/random_forest_model.sav", "rb"))
    elif model_selection == "LightGBM":
        model = pickle.load(open("Models/random_forest_model.sav", "rb"))
    
    classes = model.classes_
    df =pd.read_csv("data/data.csv")
    
    participant_selection = st.selectbox('Select participant', ('Participant 1', 'Participant 2', 'Participant 3'))

    launch = st.button('Launch simulation')



    if launch:
        
        
        chart_data = pd.DataFrame(np.array([0.2, 0.5, 0.1, 0.0, 0.1, 0.0, 0.1]), index=classes)
        st.bar_chart(chart_data)



def models():
    st.subheader("View models")
    model_selection = st.selectbox(
        'Select model',
        ('Random Forest', 'LightGBM'))


if __name__ == "__main__":
    main()