import cv2
import numpy as np

img = cv2.imread("input_separated_objects.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Red range 1
lower_red1 = np.array([0, 40, 40])
upper_red1 = np.array([10, 255, 255])

red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

# Red range 2
lower_red2 = np.array([170, 40, 40])
upper_red2 = np.array([179, 255, 255])

red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

red_mask = cv2.bitwise_or(red_mask1, red_mask2)

lower_green = np.array([35, 50, 50])
upper_green = np.array([85, 255, 255])

green_mask = cv2.inRange(hsv, lower_green, upper_green)

lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

lower_yellow = np.array([15, 40, 30])
upper_yellow = np.array([40, 255, 255])

yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

color_boxes = {
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Yellow": (0, 255, 255)
}

def detect_color(mask, color_name, image):

    box_color = color_boxes[color_name]

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:

        area = cv2.contourArea(contour)

        if area > 300:

            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                box_color,
                2
            )

            (text_width, text_height), _ = cv2.getTextSize(
                color_name,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )

            text_y = y + text_height + 5

            cv2.rectangle(
                image,
                (x, y),
                (x + text_width + 8, y + text_height + 10),
                box_color,
                -1
            )

            cv2.putText(
                image,
                color_name,
                (x + 2, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )
                


detect_color(red_mask, "Red", img)

detect_color(green_mask, "Green", img)

detect_color(blue_mask, "Blue", img)

detect_color(yellow_mask, "Yellow", img)


cv2.imshow("Color Recognition", img)

cv2.waitKey(0)
cv2.destroyAllWindows()