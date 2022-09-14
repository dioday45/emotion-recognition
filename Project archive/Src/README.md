# README

This archive contains the code we wrote for our semester project at EPFL, named "Real-time emotion recognition in VR". This archive is composed of 2 different subfolder that are described below.

## Dataset creation

This folder contains the Unity project we built to record participants data.

### Usage

1. Open the project in Unity 3D
1. Ensure Vive pro eye and facial tracker are connected and working
1. Launch the application directly in unity using "play" button
1. Commands:
   1. Enter: launch recording
   1. Spacebar: indicate apex is reached while recording 
   1. Left/right arrow: switch between AUs presented and recorded (while not recording)
1. Blendshapes will then be recorded into two .csv files under ``Assets/Data/Weights``
1. To record screen, we used to built in Unity video recorder

## Emotion recognition model

This folder contains all the files concerning the implementation of the emotion recognition models

### Cleaned dataset

Contains a cleaned version of the dataset (inconsistent data removed). 

### Data reviewing

Contains two notebook reviewing some statistics of the dataset.

### Models implementation 

contains the implementation of both models as well as a comparison between different other model (notebooks).

- Data_processing: Merge the dataset to build a single file
- Models_comparison: Compare multiple basic ML model
- LGBM: Implementation of the LightGBM model
- Random_Forest: Implementation of the Random Forest model

Due to problem in the recorded data, Participant 7 is not used for training

