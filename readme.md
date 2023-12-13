# FP-RSBP BISINDO Sign Language Translator

## Group Member

| NRP | Name |
| --- | --- |
| 5025211015 | Muhammad Daffa Ashdaqfillah |
| 5025211015 | Ulima Kultsum |
| 5025211015 | Nur Azizah |

## Description

This project is a final project for "Rekayasa Sistem Berbasis Pengetahuan (RSBP)". This project is a web-based application that can translate BISINDO sign language to Indonesian language. This application is made to help people who are not familiar with BISINDO sign language to communicate with people who are deaf. </br>

## Appoarch Method

This project employs the Object Detection method to identify hand gestures, utilizing a customized YOLO v8 dataset model. This model is designed to detect various hand gestures and provide the bounding box coordinates delineating these gestures. Once the bounding box is identified, the corresponding region of interest (ROI) containing the hand gesture is cropped. Subsequently, this cropped image undergoes further processing through a Convolutional Neural Network (CNN) model for precise classification of the detected hand gesture. The CNN model's output yields the specific label corresponding to the gesture identified. To enhance user experience, these labels are translated into Indonesian using a Rule-Based method before being displayed on the screen interface. </br>

In terms of visualization, the project harnesses MediaPipe, a tool enabling the drawing of hand gesture bounding boxes and their associated labels directly on the screen. This integration ensures users can visually comprehend the detected gestures in real-time with graphical representations. </br>

Moreover, the project is built as a web-based application using Flask, allowing seamless accessibility and interaction through a web interface. This framework facilitates the deployment of the hand gesture detection system within a browser, ensuring ease of use across various devices without necessitating complex setups or installations. </br>

## Visual Demo

### Dashboard
![dashboard](img/image.png)</br>

### Stream Youtube Detection
![yt](img/image-2.png)</br>

### Camera Detection
![run](img/image-1.png)</br>

## Step by Step Method
- Train the model using YOLOv8 with custom dataset
- Create a CNN model to classify the cropped image
- Create a Flask app to run the model
- Create a web interface using HTML and CSS
- Create feature interaction using Javascript 

## Features
- Detect hand gesture from Camera
- Detect hand gesture from Youtube video
- Switch on/off the detection
- Switch on/off the landmark
- Flip the video
- Modify Confidence Threshold
- The result accumulates the detected words over 10 sequential frames

## How to Run
- Clone this repository
- Install all the requirements
- Run the app.py file
- Open the localhost link in your browser
 
