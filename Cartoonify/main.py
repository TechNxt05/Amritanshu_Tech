import cv2
import numpy as np
import matplotlib.pyplot as plt


# Load image
def read_file(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()
    return img

filename = "9.jpeg"
img = read_file(filename)
org_img = np.copy(img)

# Create Edge Mask

def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)

    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

    return edges

line_size, blur_value = 7, 7
edges = edge_mask(img, line_size, blur_value)
plt.imshow(edges, cmap ="gray")
plt.show()

def color_quantization (img, k):
    data = np.float32(img).reshape(-1,3)

    criteria = (cv2.TermCriteria_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)

    result = center[label.flatten()]
    result = result.reshape(img.shape)

    return result

img_quantize = color_quantization (img, k=30)

plt.imshow(img_quantize)
plt.show()

# Reduce noise

blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200, sigmaSpace=200)
plt.imshow(blurred)
plt.show()

def cartoon ():
    c = cv2. bitwise_and(blurred, blurred, mask= edges)
    plt.imshow(c)
    plt.title("Cartoonified Image")
    plt.show()

    plt.imshow(org_img)
    plt.title("Original Image")
    plt.show()

cartoon()

