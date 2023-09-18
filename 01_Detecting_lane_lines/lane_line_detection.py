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


def region_of_interest(image: np.ndarray) -> np.ndarray:
    """
    This function creates a mask for the region of interest
    :param image: input image
    :return: image with the region of interest
    """
    height = image.shape[0]
    # Define the region of interest
    polygons = np.array([
        [(50, height), (500, height), (350, 190)]
    ])
    # Create a mask
    mask = np.zeros_like(image)
    # Fill the mask with the polygon
    cv2.fillPoly(mask, polygons, 255)
    # Apply the mask to the image
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image


def display_lines(masked_image: np.ndarray, hough_lines: np.ndarray) -> np.ndarray:
    """
    This function displays the lines on the input image
    :param masked_image: input image
    :param hough_lines: lines to be displayed
    :return: None
    """
    # Create a copy of the image
    line_img = np.zeros_like(masked_image)
    # Check if the lines are not empty
    if hough_lines is not None:
        # Iterate over all the lines
        for line in hough_lines:
            # Reshape the line
            x1, y1, x2, y2 = line.reshape(4)
            # Draw the line
            cv2.line(line_img, (x1, y1), (x2, y2), (255, 0, 0), 10)

    return line_img


# Load image
image = cv2.imread('images/road.jpg')
# Create a copy of the image
lane_image = np.copy(image)
# Apply Canny edge detection
canny_image = canny(lane_image)
# Apply the region of interest
cropped_image = region_of_interest(canny_image)
# Calculate the Hough lines
lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 120, np.array([]), minLineLength=40, maxLineGap=20)
# Display the lines on the image
line_image = display_lines(lane_image, lines)

cv2.imshow('result', line_image)
cv2.waitKey(0)
