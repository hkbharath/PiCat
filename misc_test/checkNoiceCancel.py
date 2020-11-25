import cv2
import numpy as np
import matplotlib.pyplot as plt

random_image_file = "^*?*:.png"
# We've used this image now, so we can't repeat it in this iteration
kernel = np.ones((5,5),np.uint8)

# We have to scale the input pixel values to the range [0, 1] for
# Keras so we divide by 255 since the image is 8-bit RGB
raw_data = cv2.imread(random_image_file)
rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
noise_cancel_data = cv2.morphologyEx(rgb_data, cv2.MORPH_OPEN, kernel)

cv2.imwrite("noce_can.png", noise_cancel_data)