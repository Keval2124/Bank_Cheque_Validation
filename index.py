from urllib.request import Request
from urllib.request import urlopen
import numpy as np
import cv2

name = "https://miro.medium.com/max/1200/0*0X8Z8EXF0mXUSLvB.jpg"
req = Request(
    url=name,
    headers={'User-Agent': 'Mozilla/5.0'}
)
req = urlopen(req)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1) # Load it as it is

cv2.imwrite('image.png', img)

from PIL import Image
from pytesseract import pytesseract

# Define path to tessaract.exe
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'

# Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract

img = 'image.png'

# Load the image
image = cv2.imread(img)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to extract the information
thresh = cv2.threshold(
    gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

txt = pytesseract.image_to_string(Image.open(
    img), lang='eng')

txt = txt.strip()
f = open("test.txt", "w")
f.write(txt)
f.close()

def text():
    payee = None
    amount = None
    lines = txt.split('\n')
    # print(lines)
    for line in lines:
        if 'pay' in line:
            payee = line.split('pay')[1]
            payee = payee.partition('_')[0]
        if 'Rupees' in line:
            amount = line.split('Rupees')[1]
            amount = amount.partition('—')[0]
            amount = "Rupess" + amount
    print("Payee:", payee)
    print("Amount:", amount)

# Print the payee's name and amount

y = 300
x = 850
h = 7500
w = 4000
signature_region = gray[y:y+h, x:x+w]

#Apply blurred to image
blurred = cv2.GaussianBlur(signature_region, (5, 5), 0)

# Apply thresholding to extract the signature
thresh2 = cv2.threshold(blurred, 60, 200, cv2.THRESH_BINARY_INV)[1]

# Find contours in the thresholded image
contours, hierarchy = cv2.findContours(
    thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Check if any contours were found
if len(contours) > 0:
    print("Signature found")
    text()
else:
    print("Signature not found")

import os
os.remove("image.png")