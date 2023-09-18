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
            x1, y1, x2, y2 = line.reshape(4)  # x1, y1, x2, y2 = line
            # Draw the line
            cv2.line(line_img, (x1, y1), (x2, y2), (255, 0, 0), 10)

    return line_img


def make_coordinates(lane_img: np.ndarray, line_parameters: np.ndarray) -> np.ndarray:
    """
    This function calculates the coordinates of the lines
    :param lane_img: input image
    :param line_parameters: parameters of the lines
    :return: coordinates of the lines
    """
    # Get the slope and intercept
    slope, intercept = line_parameters
    # Get the height of the image
    y1 = lane_img.shape[0]
    # Calculate the coordinates of the lines
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])


def average_slope_intercept(lane_img: np.ndarray, hough_lines: np.ndarray) -> np.ndarray:
    """
    This function averages the lines
    :param lane_img: input image
    :param hough_lines: lines to be averaged
    :return: averaged lines
    """
    # Create empty lists
    left_fit = []
    right_fit = []
    # Iterate over all the lines
    for line in hough_lines:
        # Reshape the line
        x1, y1, x2, y2 = line.reshape(4)
        # Fit a polynomial to the points
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        # Get the slope and intercept
        slope = parameters[0]
        intercept = parameters[1]
        # Check if the slope is negative
        if slope < 0:
            # Append the slope and intercept to the left list
            left_fit.append((slope, intercept))
        else:
            # Append the slope and intercept to the right list
            right_fit.append((slope, intercept))
    if len(left_fit) and len(right_fit):
        # Average the lines
        left_fit_average = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)
        # Calculate the coordinates of the lines
        left_line = make_coordinates(lane_img, left_fit_average)
        right_line = make_coordinates(lane_img, right_fit_average)

        return np.array([left_line, right_line])


if __name__ == '__main__':
    # Load image
    image = cv2.imread('assets/road.jpg')
    # Create a copy of the image
    lane_image = np.copy(image)
    # Apply Canny edge detection
    canny_image = canny(lane_image)
    # Apply the region of interest
    cropped_image = region_of_interest(canny_image)
    # Calculate the Hough lines
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 120, np.array([]), minLineLength=40, maxLineGap=20)
    # Average the lines (Smooth the lines)
    averaged_lines = average_slope_intercept(lane_image, lines)
    # Display the lines
    line_image = display_lines(lane_image, averaged_lines)
    # Display combined image
    combined_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

    cv2.imshow('result', combined_image)
    cv2.waitKey(0)
