# Manual GUI test

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import cv2
import easyocr
from PIL import Image, ImageTk
import csv

class TextDetectionApp:
    def __init__(self, root):
        # Initialize the TextDetectionApp class
        self.root = root
        self.root.title("Text Detection App")

        # Create image label to display loaded image
        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=10, pady=10)

        # Create buttons for loading, detecting text, saving image, and resetting filters
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5)

        self.detect_button = tk.Button(self.root, text="Detect Text", command=self.detect_text)
        self.detect_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Text", command=self.save_image)
        self.save_button.pack(pady=5)

        # Initialize EasyOCR reader for text detection
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.image = None

        # Define image preprocessing options
        self.preprocess_options = {
            "Clear": self.no_filter,
            "Grayscale": cv2.COLOR_BGR2GRAY,
            "Blur": (cv2.GaussianBlur, (5, 5), 0),
            "Sharpen": (self.apply_sharpen_filter,),
        }

        self.preprocess_options.update({
            "Opening": self.apply_opening_filter,
            "Closing": self.apply_closing_filter,
            "Erosion": self.apply_erosion_filter,
            "Dilation": self.apply_dilation_filter,
        })

        # Initialize default preprocessing option
        self.selected_preprocess = tk.StringVar()
        self.selected_preprocess.set("Clear")  # Default selection

        # Create radio buttons for selecting preprocessing options
        preprocess_frame = tk.Frame(self.root)
        preprocess_frame.pack()

        self.preprocess_buttons = {}  # Dictionary to store preprocess buttons

        for option in self.preprocess_options:
            button = tk.Button(preprocess_frame, text=option, command=lambda op=option: self.update_display(op))
            button.pack(side=tk.LEFT)
            self.preprocess_buttons[option] = button

        self.threshold_label = tk.Label(self.root, text="Threshold:")
        self.threshold_label.pack(pady=(5, 0))
        self.threshold_scale = tk.Scale(self.root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=self.update_threshold)
        self.threshold_scale.pack(pady=(0, 10))
        self.threshold_scale.set(0.50)  # Default threshold value

        # Disable the bottom row buttons upon startup
        self.disable_bottom_row_buttons()

        # Disable detect and save buttons initially
        self.detect_button.config(state="disabled")
        self.save_button.config(state="disabled")

    def load_image(self):
        # Load an image using file dialog.
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.original_image = self.image.copy()  # Store a copy of the original image

            # Get the screen width and height
            screen_width = self.root.winfo_screenwidth() / 2
            screen_height = self.root.winfo_screenheight() / 2

            # Get the width and height of the loaded image
            img_height, img_width, _ = self.image.shape

            # Calculate the scaling factor
            scale_factor = min(screen_width / img_width, screen_height / img_height)

            # Resize the image while preserving aspect ratio
            self.image = cv2.resize(self.image, (int(img_width * scale_factor), int(img_height * scale_factor)))

            self.display_image()
            self.enable_buttons()
            self.enable_bottom_row_buttons()

    def display_image(self):
        # Display the loaded image in the GUI.
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        self.image_label.configure(image=image_tk)
        self.image_label.image = image_tk

    def update_display(self, option):
    # Update the displayed image based on the selected preprocessing option.
        if self.image is not None:
            if option == "Clear":
                self.image = self.original_image.copy()
                self.display_image()
                self.enable_buttons()
                self.enable_bottom_row_buttons()
                return

            preprocess_method = self.preprocess_options[option]
            if isinstance(preprocess_method, tuple):
                if len(preprocess_method) == 3:
                    filtered_image = preprocess_method[0](self.image, preprocess_method[1], preprocess_method[2])
                else:
                    filtered_image = preprocess_method[0](self.image)
            elif callable(preprocess_method):  # Check if preprocess_method is a callable method
                if preprocess_method == cv2.COLOR_BGR2GRAY:  # Check if preprocess_method is grayscale conversion
                    filtered_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                else:
                    filtered_image = preprocess_method(self.image)
            else:
                # Skip if preprocess_method is not callable
                return

            # Display the filtered image
            self.image = filtered_image
            self.display_image()
            self.enable_buttons()


    def detect_text(self):
        # Detect text in the loaded image
        if self.image is None:
            print("Error: Please load an image first.")
            return

        # Capture threshold value from the scale widget
        threshold = self.threshold_scale.get()

        # Disable all buttons
        self.disable_buttons()

        if len(self.image.shape) == 3 and self.image.shape[2] == 3:
            preprocessed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            preprocessed_image = self.image

        # Clear existing rectangles and text
        self.image = self.original_image.copy()
        self.display_image()

        # Perform text detection
        text_results = self.reader.readtext(preprocessed_image)
        for result in text_results:
            print(result)  # Print the tuple
            if len(result) >= 3:  # Check if the tuple has at least three elements
                bbox, text, confidence = result[:3]  # Extract the first three elements
                method = ""  # Default value for method
                if len(result) >= 4:
                    method = result[3]  # Extract the fourth element if available
                if confidence > threshold:  # Apply threshold filtering
                    # Extract coordinates from the bounding box
                    pt1 = (int(bbox[0][0]), int(bbox[0][1]))
                    pt2 = (int(bbox[2][0]), int(bbox[2][1]))
                    cv2.rectangle(self.image, pt1, pt2, (0, 0, 255), 2)
                    cv2.putText(self.image, text, pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        self.display_image()

        # Print a new line after printing all tuples
        print()

        self.disable_bottom_besides_clear()  # Disable bottom row buttons besides clear

    def update_threshold(self, value):
        self.threshold = float(value)

    def save_image(self):
        # Save the detected text data to a CSV file.
        if self.image is None:
            print("Error: Please load an image first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            # Perform text detection
            if len(self.image.shape) == 3 and self.image.shape[2] == 3:
                preprocessed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            else:
                preprocessed_image = self.image
            text_results = self.reader.readtext(preprocessed_image)

            # Save text data to CSV
            self.save_text_data_to_csv(text_results, file_path)
            messagebox.showinfo("Success", "Text data saved to CSV successfully.")


    def no_filter(self, image):
        # Return the original image without any preprocessing.
        return image

    def apply_sharpen_filter(self, image):
        # Apply sharpening filter to the image.
        sharpen_kernel = np.array([[-1, -1, -1],
                                   [-1, 9, -1],
                                   [-1, -1, -1]])
        return cv2.filter2D(image, -1, sharpen_kernel)

    # new filters start
    def apply_opening_filter(self, image):
        # Apply opening filter to the image
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    def apply_closing_filter(self, image):
        # Apply closing filter to the image
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    def apply_erosion_filter(self, image):
        # Apply erosion filter to the image
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    def apply_dilation_filter(self, image):
        # Apply dilation filter to the image
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)
    # new filters end

    def disable_bottom_row_buttons(self):
        # Disable buttons in the bottom row (excluding "Clear")
        for option, button in self.preprocess_buttons.items():
            if option:
                button.config(state="disabled")

    def disable_bottom_besides_clear(self):
        # Disable buttons in the bottom row (excluding "Clear")
        for option, button in self.preprocess_buttons.items():
            if option != "Clear":
                button.config(state="disabled")

    def enable_bottom_row_buttons(self):
        # Disable buttons in the bottom row (excluding "Clear")
        for option, button in self.preprocess_buttons.items():
            if option:
                button.config(state="normal")   

    def disable_buttons(self):
        # Disable all buttons except the "Clear" button
        self.detect_button.config(state="disabled")
        self.load_button.config(state="disabled")
        # self.save_button.config(state="disabled")

    def enable_buttons(self):
        # Enable all buttons
        self.detect_button.config(state="normal")
        self.load_button.config(state="normal")
        self.save_button.config(state="normal")

        #for new buttons
        for option, button in self.preprocess_buttons.items():
            if option in ["Opening", "Closing", "Erosion", "Dilation"]:
                button.config(state="normal")

    # for saving data
    def save_text_data_to_csv(self, text_results, file_path):
        # Save the text data along with their confidence levels to a CSV file
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write the text data and confidence levels
            writer.writerow(["Text", "Confidence Level"])
            for result in text_results:
                if len(result) >= 3:  # Check if the tuple has at least three elements
                    text, confidence = result[1], result[2]  # Extract text and confidence
                    writer.writerow([text, confidence])

def main():
    # Create the Tkinter application and run the TextDetectionApp.

    root = tk.Tk()
    app = TextDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
