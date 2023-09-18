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
    #masked_image = cv2.bitwise_and(image, mask)

    return mask


# Load image
image = cv2.imread('images/road.jpg')
# Create a copy of the image
lane_image = np.copy(image)
# Apply Canny edge detection
canny_image = canny(lane_image)

#plt.imshow(canny_image)
#plt.show()
