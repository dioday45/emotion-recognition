import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import animation
from pathlib2 import Path
from sklearn.metrics import plot_confusion_matrix, precision_score, recall_score, accuracy_score, f1_score

def main():
    st.title("Emotion recognition evaluation")

    st.sidebar.title("Settings")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Main page", "Real-time evaluation simulation", "Models overview"])

    if app_mode == "Main page":
        st.sidebar.success('Next, try selecting "Real-time evaluation simulation".')
        main_page()

    elif app_mode == "Real-time evaluation simulation":
        eval_visu()

    elif app_mode == "Models overview":
        models_metrics() 

    return None


def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()


def main_page():
    intro_markdown = read_markdown_file("markdown_files/main_page.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)


def selections():
    #Selection of model, participant and recording
    model_selection = st.selectbox('Select model', {'Random Forest', 'LightGBM'})

    if model_selection == 'Random Forest' :
        model = pickle.load(open("Models/random_forest_model.sav", "rb"))
    elif model_selection == "LightGBM":
        model = pickle.load(open("Models/lgbm_model.sav", "rb"))
    
    participant_selection = st.selectbox('Select participant', ('Participant 1', 'Participant 2'))
    recording_selection = st.selectbox('Select recording number', ('Recording 1', 'Recording 2'))

    #Get data paths from data folder
    data_path = "data/{participant}/{recording}/data.csv".format(participant=participant_selection, recording=recording_selection)
    truth_path = "data/{participant}/{recording}/truth.csv".format(participant=participant_selection, recording=recording_selection)
    video_path = "data/{participant}/{recording}/video.mp4".format(participant=participant_selection, recording=recording_selection)
    return data_path, truth_path, video_path, model


def eval_visu():
    st.header("Real-time evaluation simulation")
    st.subheader("Settings selection")
    data_path, truth_path, video_path, model = selections()

    #Video of the selected participant
    st.subheader("Participant video")
    st.write("Here you can see the corresponding video to the selected participant. The corresponding data are recorded at a frequency of 50Hz during the 25 seconds of the recording (timer in red).")
    st.write("See below to run the model on this data.")
    st.video(video_path)


    st.subheader("Simulation")
    st.markdown("To start the simulation, press the button below.")
    classes = model.classes_
    df = pd.read_csv(data_path, index_col=0) #raw recorded data (simulating what would be the data of a real-time implementation)
    truth = pd.read_csv(truth_path, index_col=0)["Expression"] #True emotion of the data above

    #Iteratively run the model on all the data, and then create an animation of the plots of the predicted emotions of each rows
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


def models_metrics():
    st.header("Models metrics overview")
    st.subheader("Settings selection")
    data_path, truth_path, video_path, model = selections()
    df = pd.read_csv(data_path, index_col=0) 
    truth = pd.read_csv(truth_path, index_col=0)["Expression"]

    st.subheader("General metrics")
    st.markdown("You can see below some basic metrics of the model applied to the selected participant.")
    pred = model.predict(df)
    st.write("Accuracy: ", accuracy_score(truth, pred).round(2))
    st.write("Precision: ", precision_score(truth, pred, labels=model.classes_, average='macro').round(2))
    st.write("Recall: ", recall_score(truth, pred, labels=model.classes_, average='macro').round(2))
    st.write("F1 score: ", f1_score(truth, pred, average='macro').round(2))

    st.subheader("Confusion matrix")
    plot_confusion_matrix(model, df, truth, display_labels=model.classes_, cmap='BuPu')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    


if __name__ == "__main__":
    main()