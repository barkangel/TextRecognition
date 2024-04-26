# Sample program to test text scanning from an image. Not utlized in program, just an example of how to scan text.

import cv2
import easyocr
import matplotlib.pyplot as plt
# Reading the image
image_path = 'test3.png'

img = cv2.imread(image_path)

# Instance of our text detector
reader = easyocr.Reader(['en'], gpu=True)

# Detecting text on image
text_ = reader.readtext(img)
threshold = 0.25

# draw bounding box and text onto image

for t in text_:
    print(t)
    bbox, text, score = t

    # sample: ([[166, 126], [448, 126], [448, 182], [166, 182]], 'ROAD CLOSED', 0.9994066640174729)
    # first element: upper left x, upper left y bbox[0]
    # third element: bottom right x, bottom right y bbox[2]
    # last element: confidence value
    
    if score > threshold:
        cv2.rectangle(img, bbox[0], bbox[2], (0, 0, 255), 5)
        # img, text, upper location, font, size, color, thickness
        cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)


plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()