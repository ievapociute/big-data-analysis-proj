from multiprocessing import Pool, cpu_count
import cv2
import numpy as np
import os
import time

def find_thresh(grayscale):
    hist = cv2.calcHist([grayscale], [0], None, [256], [0, 256]).flatten() 
    cum_hist_norm = np.cumsum(hist) / hist.sum()
    threshold = np.searchsorted(cum_hist_norm, 0.5)
    black_pixels = hist[:threshold].sum()
    return threshold, black_pixels


def salt_pepp_noise(image, noisy_pixels):
    noisy_image = image.copy()
    height, width, _ = noisy_image.shape
    
    row_indices = np.random.randint(0, height, noisy_pixels)
    col_indices = np.random.randint(0, width, noisy_pixels)
    
    noise_values = np.random.choice([0, 255], size=(noisy_pixels, 3))
    
    noisy_image[row_indices, col_indices] = noise_values
    
    return noisy_image


def transform_image_bw_noise(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold, black_pixels = find_thresh(gray)
    bnw_image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
    noisy_image = salt_pepp_noise(image, int(0.1 * black_pixels))
    return bnw_image, noisy_image

def transform_image_blur(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred

def save_image_bw_noise(image_path, output_dir):
    image = cv2.imread(image_path)
    bnw_image, noisy_image = transform_image_bw_noise(image)
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    cv2.imwrite(os.path.join(output_dir, f"{base_name}_bnw.jpg"), bnw_image)
    cv2.imwrite(os.path.join(output_dir, f"{base_name}_noisy.jpg"), noisy_image)


def save_image_blur(image_path, output_dir):
    image = cv2.imread(image_path)
    blurred = transform_image_blur(image)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    cv2.imwrite(os.path.join(output_dir, f"{base_name}_blurred.jpg"), blurred)


def process_images_parallel(input_dir, output_dir, transform_and_save_image):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_paths = [
        os.path.join(input_dir, f) for f in os.listdir(input_dir) 
        if f.endswith('.jpg')
        ]
    
    with Pool(processes=cpu_count()) as pool:
        pool.starmap(
            transform_and_save_image, 
            [(path, output_dir) for path in image_paths]
            )


if __name__ == "__main__":
    input_dir = "input"
    output_dir = "output"
    
    start_time = time.time()
    process_images_parallel(input_dir, output_dir, save_image_bw_noise)
    
    print(f"B&W and noise Processing completed in {time.time() - start_time:.2f} seconds.")

    start_time = time.time()
    process_images_parallel(input_dir, output_dir, save_image_blur)

    print(f"Blur Processing completed in {time.time() - start_time:.2f} seconds.")
