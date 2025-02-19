### in this code i am calculating calibration constant. first applying threshold. then setting the row value to mid row
## i am finding the pixel value where i become 0 from 255, that would be first side of square, then repeating this from the other side of square
## in that way i got the dimension corresponding to two sides of square and take out the differnce between them and then find out the value of K
## by dividing the pixel difference with 150mm and do this for all the three images and then plot the k value against height of the photograph.

import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def calculate_calibration_constant(file_path, actual_side_mm=150, threshold_value=128):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    binary_image = gray.copy()
    for i in range(h):
        for j in range(w):
            if gray[i, j] < threshold_value:
                binary_image[i, j] = 0
            else:
                binary_image[i, j] = 255

    plt.figure()
    plt.imshow(binary_image, cmap='gray')
    plt.title("Thresholded Image (for Calibration)")
    plt.axis("off")
    plt.show()

    mid_row = binary_image[h // 2]
    left_index = None
    right_index = None
    for i in range(w):
        if mid_row[i] == 0:
            left_index = i
            break
    for i in range(w - 1, -1, -1):
        if mid_row[i] == 0:
            right_index = i
            break

    pixel_distance = right_index - left_index + 1
    K = actual_side_mm / pixel_distance
    print("Calibration constant (mm per pixel):", K)
    return K


file_paths = [
    r"/home/idc2025/Downloads/IMG_20250215_071652.jpg",
    r"/home/idc2025/Downloads/IMG_20250215_071952.jpg",
    r"/home/idc2025/Downloads/IMG_20250215_072357.jpg"
]
heights = [15, 25, 35]


threshold_values = [200, 188, 205]


calibration_constants = []
for i, path in enumerate(file_paths):
    print(f"\n=== Processing Calibration for Image {i+1} with threshold {threshold_values[i]} ===")
    K = calculate_calibration_constant(path, threshold_value=threshold_values[i])
    calibration_constants.append(K)


plt.figure()
plt.plot(heights, calibration_constants, marker='o', linestyle='-')
plt.xlabel("Height (cm)")
plt.ylabel("Calibration Constant (mm per pixel)")
plt.title("Calibration Constant vs Height")
plt.grid(True)
plt.savefig("calibration_graph.jpg")
plt.show()


for i, path in enumerate(file_paths):
    output_path = f"processed_image_{i+1}.jpg"
    cv2.imwrite(output_path, cv2.imread(path))  
    print(f"Saved: {output_path}")



