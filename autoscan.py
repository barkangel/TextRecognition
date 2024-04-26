# Automatic text scanning of folder full of images. Useful for dataset. 

import os
import cv2
import easyocr
import numpy as np

def apply_filter(image, filter_type):
    if filter_type == 1:
        # Sharpen
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        return sharpened
    elif filter_type == 2:
        # Gaussian Blur
        blurred = cv2.GaussianBlur(image, (5,5), 0)
        return blurred
    elif filter_type == 3:
        # Opening
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return opening
    elif filter_type == 4:
        # Closing
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        return closing
    elif filter_type == 5:
        # Erosion
        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(image,kernel,iterations = 1)
        return erosion
    elif filter_type == 6:
        # Dilation
        kernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(image,kernel,iterations = 1)
        return dilation
    else:
        return image  # No filter

def ocr_image(image_path, filter_type):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        raise ValueError(f"Failed to load image from {image_path}")

    # Apply selected filter
    filtered_image = apply_filter(image, filter_type)

    # Convert the filtered image to grayscale
    gray = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)

    # Initialize the OCR reader
    reader = easyocr.Reader(['en'])

    # Perform OCR on the grayscale image
    result = reader.readtext(gray)

    # Extract the text, confidence values, and bounding box coordinates
    text_data = []
    for detection in result:
        text = detection[1]
        confidence = detection[2]
        bbox = detection[0]
        text_data.append((text, confidence, bbox))

    return text_data

def scan_images(folder_path, output_file, filter_type):
    total_images = len([filename for filename in os.listdir(folder_path) if filename.endswith(('.jpg', '.jpeg', '.png'))])
    scanned_images = 0

    with open(output_file, 'w') as f:
        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                scanned_images += 1
                # Construct the full path to the image file
                image_path = os.path.join(folder_path, filename)

                try:
                    # Perform OCR on the image after applying the selected filter
                    text_data = ocr_image(image_path, filter_type)

                    # Write the extracted text, confidence values, and bounding box coordinates to the output file
                    f.write(f"File: {filename}\n")
                    for text, confidence, bbox in text_data:
                        #f.write(f"Text: {text}, Confidence: {confidence}, Bounding Box: {bbox}\n")
                        f.write(f"Text: {text}, Confidence: {confidence}\n")
                    f.write('\n')

                    # Print scan progress to the terminal
                    print(f"Scanning... ({scanned_images}/{total_images}) - Filter type: {filter_type}")
                except ValueError as e:
                    print(e)

def main():
    # Prompt the user to enter the folder path containing images
    folder_path = input("Enter the folder path containing images: ")

    # Validate the folder path
    if not os.path.exists(folder_path):
        print("Invalid folder path. Please provide a valid path.")
        return

    # Prompt the user to select a filter
    print("Select a filter (enter 0 for no filter, 1-6 for different filters):")
    print("0 - No filter, 1 - Sharpen, 2 - Gaussian Blur, 3 - Opening, 4 - Closing, 5 - Erosion, 6 - Dilation")
    filter_type = input("Enter the number corresponding to the filter: ")

    # Convert filter_type to an integer
    filter_type = int(filter_type)

    # Validate the filter type
    if filter_type not in range(0, 7):
        print("Invalid filter type. Please enter a number between 0 and 6.")
        return

    # Prompt the user to enter the output file name
    output_file = input("Enter the output file name (including extension): ")

    # Scan images in the folder for text after applying the selected filter (if any) and save to a text file
    scan_images(folder_path, output_file, filter_type)

    print()
    print("Success!")


if __name__ == "__main__":
    main()
