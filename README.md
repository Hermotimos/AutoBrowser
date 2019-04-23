# AutoBrowser

## Table of contents
* [General info](#general-info)  
* [Technologies](#technologies)  
* [Setup](#setup)  
* [Features](#features)
* [Content](#content)  
* [Status](#status)  


## General info
This program automatizes the use of a browsing/scraping program created and used by a certain company I occasionally work for.  
It was created in th scope of my free time activity for personal use only (not commercially), mostly with the aim of improving my Python and general programming skills.

## Technologies
Python 3.7 (especially pyautogui module)

## Setup
Program created and run in IDE (PyCharm 2019.1.1 Community Edition) under Windows 7.  
May be converted to .exe with pyinstaller.

## Features
Automated handling of a scraping program and browsed pages opened inside it.

## Content

### main.py
Main module.
### browsing_flow.py
Defines steps of automated browsing flow.
### report_class.py
Defines class that prints out log during execution and saves it to a report file afterwards.
### movements_and_clicks.py
Functions for reactions to site features.
### image_processing.py
Functions for recognition of site features.

## Status
TODO:  
    * Create another class for browsed pages countdown. Class would prevent resetting of browsed pages count by program recalibration in cases of RecursionError in functions.  