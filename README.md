# Capstone1
An app that visualizes data from Detectors Inc Devices and compares them to known fire and light sources.


This aplication is built using AppJar and is intended to be packaged by pyinstaller.

Background: Detectors Incorporated Flame detectors first generation devices save records of the last 5 fires in memory and can output a constant stream of data to a seperate labview VI on a computer for recording as a .txt file. 


The app allows the user to select a .txt file recorded from the detectors and ingests this data, cleans it of errors made during communication, as the communication protocol between device and labview VI is error prone, and first creates a pandas dataframe and a plot is generated from it which is automatically scaled to fit within the app window. The useful sensor data is then extracted and made into two numpy arrays one for IR and one for UV and those are stacked depth wise and transformed into  RGB images, (stacked vertically further to make it more easily visible). 

since this does not always fit within the app window, a 600 element splice is created and displayed along with two buttoms which allow the user to scroll through the data, using hte already scaled graph s a guide.

lastly a dropdown menu allows the user to select and display pre-stored data from known sources for which to compare the 'color' and pattern of the recorded fires of various fuel sources and lights known to be plroblematic. thus allowing the user to identify possible sources of false alarms or make useful feedback on observed data.
