# Import all the necessary packages
import cv2
import numpy as np
import matplotlib.pyplot as plt


def canny(image: np.ndarray) -> np.ndarray:
    """
    This function applies Canny edge detection to the input image
    :param image: input image
    :return: image with edges detected
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Reduce noise in the image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply Canny edge detection
    canny_img = cv2.Canny(blur, 50, 150)

    return canny_img


