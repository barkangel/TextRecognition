# TextRecognition
## Description:
A collection of Digital Image Processing programs for my college class to detect text out of an image, utilizing image preprocessing techniques such as:  

- (0) No Filter
- (1) Sharpness
- (2) Gaussian Blur
- (3) Opening
- (4) Closing
- (5) Erosion
- (6) Dilation

Utilizing 2 main methods: 
1. Manual GUI for one image at a time.
2. Automatic command line that handles large datasets.

## Files:
- gui.py : Manual TKinter GUI where you can upload images, see filters in real time, and scan text that outputs to terminal or file. 
- autoscan.py : Automatic text scanning of folder full of images. Provide path, select filter options (0-6) and enter output file name.
- scan_text.py : Sample program to test text scanning, not utilized.
- diff.py : Compares image's multiple filter output files after multiple runs. 
- average.py : Calculates and returns the average confidence value of provided output file. Works mainly with autoscan.py output files.

## Folders:
- input : put datasets/images here you want to scan text from.
- output : This is where GUI output goes. Autoscan generated output files result in parent directory. 

## How to run:
- put images you want to scan in input folder
- install requirements.txt
- py (filename) to run any of the files. All are command line based besides gui.py.
