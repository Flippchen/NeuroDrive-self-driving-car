import cv2
import numpy as np

from lane_line_detection import canny, region_of_interest, display_lines, average_slope_intercept

# Make sure to adjust the polygons to the video size


cap = cv2.VideoCapture("assets/video.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        canny_img = canny(frame)
        cropped_img = region_of_interest(canny_img)
        hough_lines = cv2.HoughLinesP(cropped_img, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
        averaged_lines = average_slope_intercept(frame, hough_lines)
        line_img = display_lines(frame, averaged_lines)
        combo_img = cv2.addWeighted(frame, 0.8, line_img, 1, 1)
        cv2.imshow("result", combo_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
