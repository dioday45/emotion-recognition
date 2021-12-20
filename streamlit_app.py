import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import animation

def main():
    st.title("Emotion recognition evaluation")

    st.sidebar.title("Settings")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Main page", "Real-time evaluation simulation", "Models overview"])

    if app_mode == "Main page":
        st.sidebar.success('Next, try selecting "Real-time evaluation simulation".')
        main_page()

    elif app_mode == "Real-time evaluation simulation":
        eval()

    elif app_mode == "Models overview":
        models()

    return None

def main_page():
    st.markdown("### TODO")



def eval():
    st.subheader("Real-time evaluation simulation")

    model_selection = st.selectbox('Select model', {'Random Forest', 'LightGBM'})

    if model_selection == 'Random Forest' :
        model = pickle.load(open("Models/random_forest_model.sav", "rb"))
    elif model_selection == "LightGBM":
        model = pickle.load(open("Models/random_forest_model.sav", "rb"))
    
    participant_selection = st.selectbox('Select participant', ('Participant 1', 'Participant 2', 'Participant 3'))

    classes = model.classes_
    df =pd.read_csv("data/data.csv") ## TODO : modify in function of selected participant
    

    launch = st.button('Launch simulation')    
    if launch:
        progress_bar = st.progress(0)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_ylim(0, 1)
        plot_bar = plt.bar(classes, model.predict_proba(df.iloc[[0]])[0,:])
        data_len = len(df.index)
        predicted_df = model.predict_proba(df)
        txt = ax.text(.05,.9, "test")

        def gif_computation(idx):
            progress_bar.progress(idx/data_len)
            txt.set_text("Predicted expression : {}".format(classes[np.argmax(predicted_df[idx,:])]))
            for rect, h in zip(plot_bar, predicted_df[idx,:]):
                rect.set_height(h)

        anim = animation.FuncAnimation(fig, gif_computation, frames=data_len, blit=False)
        anim.save('Simulations/simulation.mp4', animation.FFMpegWriter(fps=50))
        progress_bar.progress(1.0)
        st.success("You can now play the visualization simulation")
        st.video("Simulations/simulation.mp4")


    show_video = st.checkbox("Show participant video")
    if show_video:
        st.write("Here you can see the corresponding video")
        st.video("data/Expression_recording023.mp4")




def models():
    st.subheader("View models")
    model_selection = st.selectbox(
        'Select model',
        ('Random Forest', 'LightGBM'))


if __name__ == "__main__":
    main()