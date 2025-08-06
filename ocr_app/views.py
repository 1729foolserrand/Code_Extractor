import os

import cv2
import pytesseract
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from PIL import Image


def preprocess_image(image_path):
    # Read image with OpenCV
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Resize for better clarity
    resized = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Apply median blur
    blurred = cv2.medianBlur(resized, 3)

    # Dilate text to strengthen character edges
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(blurred, kernel, iterations=1)

    # Save processed image temporarily
    processed_path = os.path.join(settings.MEDIA_ROOT, "processed.png")
    cv2.imwrite(processed_path, dilated)
    return processed_path


def extract_text(image_path):
    # Use Tesseract to extract text
    custom_config = r"--oem 1 --psm 6"
    text = pytesseract.image_to_string(Image.open(image_path), config=custom_config)
    return text


def upload_image(request):
    if request.method == "POST" and request.FILES["image"]:
        uploaded_file = request.FILES["image"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        image_path = fs.path(filename)

        # Preprocess the image
        processed_path = preprocess_image(image_path)

        # Extract text
        extracted_text = extract_text(processed_path)

        context = {
            "text": extracted_text,
            "filename": filename,
        }
        return render(request, "ocr_app/index.html", context)
    return render(request, "ocr_app/index.html")
