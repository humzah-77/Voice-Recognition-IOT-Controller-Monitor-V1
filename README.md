# Voice-Recognition-IOT-Controller-Monitor-V1
**Warning** Must have pyaudio, python speech_recognition and pyttsx3 installed on your machine for this to run
You must also have an Arduino cloud account along with the plan that allows you to make apis

All Variable, Things, Devices and Dashboards must be created and configured in the cloud 

you must make an API on the cloud website and get the ClienID and ClientSecret(Plese keep these two secure and private)

**My code has the clientID/Secret omited along with any thingID and PropertyID**

This project is *LUCY* a prototype Python software that controls my Arduino tasks using voice recognition and the Arduino cloud API.

# What is used<img width="562" alt="Screen Shot 2021-12-01 at 2 31 40 AM" src="https://user-images.githubusercontent.com/58381410/144190836-588f6000-48ea-4f21-9058-93159d5aa88d.png">


## Hardware
Arduino Nano 33 IOT

DTH11 Temperature and Humidity Sensor

3 x LED Lights

## Software

Python

Arduino IDE

Arduino Cloud 

Arduino CLoud API

# How it works

The code listens for a voice and records it into a string. If the string does not include the name "lucy" in it then it is discarded and the program listens for a new command. If the term lucy is in the command it pases out the name and checks the rest of the string for one of the commands. 

The program currently returns my name, returns 3 different values from the DTH11 temperature and humidity sensor and turns an LED on and off.

The proram communicates with the arduio through api calls fro the arduino cloud

.<img width="343" alt="Screen Shot 2021-12-01 at 2 33 03 AM" src="https://user-images.githubusercontent.com/58381410/144191041-3dce77af-a5cd-4e86-8afc-42ed29768527.png">
