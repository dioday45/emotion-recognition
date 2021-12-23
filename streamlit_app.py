import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import animation
from pathlib2 import Path

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

def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

def main_page():
    intro_markdown = read_markdown_file("markdown_files/main_page.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)




def eval():
    st.subheader("Real-time evaluation simulation")

 
    model_selection = st.selectbox('Select model', {'Random Forest', 'LightGBM'})

    if model_selection == 'Random Forest' :
        model = pickle.load(open("Models/random_forest_model.sav", "rb"))
    elif model_selection == "LightGBM":
        model = pickle.load(open("Models/lgbm_model.sav", "rb"))
    
    participant_selection = st.selectbox('Select participant', ('Participant 1', 'Participant 2'))
    recording_selection = st.selectbox('Select recording number', ('Recording 1', 'Recording 2'))

    data_path = "data/{participant}/{recording}/data.csv".format(participant=participant_selection, recording=recording_selection)
    truth_path = "data/{participant}/{recording}/truth.csv".format(participant=participant_selection, recording=recording_selection)
    video_path = "data/{participant}/{recording}/video.mp4".format(participant=participant_selection, recording=recording_selection)

    st.markdown("You can start the simulation by pressing the button below.")

    classes = model.classes_

    df = pd.read_csv(data_path, index_col=0) ## TODO : modify in function of selected participant    
    truth = pd.read_csv(truth_path, index_col=0)["Expression"]

    launch = st.button('Launch simulation')    
    if launch:
        st.info("Data is being processed, this can take some time so don't panic !")
        progress_bar = st.progress(0)
        fig = plt.figure()
        plt.style.use('bmh')
        ax = fig.add_subplot(1,1,1)
        ax.set_ylim(0, 1)
        plot_bar = plt.bar(classes, model.predict_proba(df.iloc[[0]])[0,:])
        data_len = len(df.index)
        predicted_df = model.predict_proba(df)
        txt_pred = ax.text(.05,.9, "Predicted expression")
        txt_truth = ax.text(.05, .8, "True expression")


        def gif_computation(idx):
            progress_bar.progress(idx/data_len)
            txt_pred.set_text("Predicted expression : {}".format(classes[np.argmax(predicted_df[idx,:])]))
            txt_truth.set_text("True expression : {}".format(truth[idx]))
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
        st.video(video_path)




def models():
    st.subheader("View models")
    model_selection = st.selectbox(
        'Select model',
        ('Random Forest', 'LightGBM'))

    st.subheader("Confusion matrix")

    if model_selection == 'Random Forest' :
        model = pickle.load(open("Models/random_forest_model.sav", "rb"))
        cm = st.image("confusion_matrix/rf_cm.png")
    elif model_selection == "LightGBM":
        model = pickle.load(open("Models/random_forest_model.sav", "rb"))
        cm = st.image("confusion_matrix/lgb_cm.png")

    st.subheader("TODO: add statistics about models")


if __name__ == "__main__":
    main()