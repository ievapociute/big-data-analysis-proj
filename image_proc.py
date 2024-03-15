import cv2
import numpy as np
path = '667626_18933d713e.jpg'
image = cv2.imread(path)

# black and white
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #to grayscale

# find the threshold value using the grayscale image
def find_thresh(grayscale):
    hist = cv2.calcHist([grayscale], [0], None, [256], [0, 256])
    hist_norm = hist/hist.sum()
    black_pixels = 0
    threshold = 0
    bl_fraction = 0
    for i in range(len(hist_norm)):
        bl_fraction += hist_norm[i]
        black_pixels += hist[i]
        if bl_fraction >= 0.5:
            threshold = i
            break
    return threshold, black_pixels[0]

(threshold, black_pixels) = find_thresh(gray_image)

(thresh, bnw_image) = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

# image blurring
# Gaussian Blurring
gaus_blur = cv2.GaussianBlur(image, (5,5),0) #chose random kernel? not specified in the exercise

# averaging
#avging = cv2.blur(image,(5,5))

# Median blurring
#med_blur = cv2.medianBlur(image,5)

# adding noise
# salt and pepper noise
def salt_pepp_noise(image, noisy_pixels):
    noisy_image = image.copy()
    height, width, _ = noisy_image.shape
    for pixel in range(noisy_pixels):
        row, col = np.random.randint(0, height), np.random.randint(0, width)
        if np.random.rand() < 0.5:
            noisy_image[row, col] = [0, 0, 0]
        else:
            noisy_image[row, col] = [255, 255, 255]
    return noisy_image
noisy_image = salt_pepp_noise(image, int(0.1*black_pixels))

# view images
#cv2.imshow('Black white image', bnw_image)
#cv2.imshow('Original image', image)
#cv2.imshow('Gaussian blur', gaus_blur)
#cv2.imshow('Salt and pepper noise', noisy_image)

#cv2.waitKey(0)
#cv2.destroyAllWindows()

# export images
name = '.'.join(path.split('.')[:-1])
cv2.imwrite(f'{name}_bnw.jpg', bnw_image)
cv2.imwrite(f'{name}_blur.jpg', gaus_blur)
cv2.imwrite(f'{name}_noise.jpg', noisy_image)

