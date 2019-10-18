# BMon_desktop
Desktop client for a babymonitor built from a Raspberry Pi.

## About the babymonitor
The baby monitor is built from an Raspberry Pi.
The Raspberry Pi has a camera sensor without infrared sensor connected to it. Also infrared LEDs, a DHT22 humidity and temperature sensor and a microphone.
The Pi streams the camera input as MJPEG and the microphone input as MP3. The data coming from the DHT22 sensor is send via UDP Broadcast.
The Pi also opens an WiFi AP.

## About the client
This application is written in python using kivy to make use of kivys crossplatform abilities.
The client device needs to connect to the WiFi AP of the baby monitor device. 
After that the client software reads and displays/plays the MJPEG and MP3 stream.
Both Audio/Video can be disabled/enabled using this application.
