# -*- coding: utf-8 -*-
"""ML-DD.ipynb

Original file is located at
    https://colab.research.google.com/drive/1sQat-qZ8L1zCzZJNPhQmZQZvLLBZM_TP

***Deepfake Detection with Python***
"""

#!pip install mtcnn

import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd
import glob2
import os, fnmatch
from pathlib import Path
# import mtcnn
from mtcnn.mtcnn import MTCNN

def extract_multiple_videos(intput_filenames, image_path_infile):
    """Extract video files into sequence of images."""
    i = 1  # Counter of first video
    # Iterate file names:
    cap = cv2.VideoCapture('your_video_file_path.avi' or intput_filenames)
    if (cap.isOpened()== False):
        print("Error opening file")
    # Keep iterating break
    while True:
        ret, frame = cap.read()  # Read frame from first video

        if ret:
            cv2.imwrite(os.path.join(image_path_infile , str(i) + '.jpg'), frame)  # Write frame to JPEG file (1.jpg, 2.jpg, ...)
# you can uncomment this line if you want to view them.
#           cv2.imshow('frame', frame)  # Display frame for testing
            i += 1 # Advance file counter
        else:
            # Break the interal loop when res status is False.
            break
    cv2.waitKey(50) #Wait 50msec
    cap.release()

# Define the paths for your fake and real video files
fake_video_name = 'path/to/your/fake_video.mp4' # Replace with the actual path to your fake video
real_video_name = 'path/to/your/real_video.mp4' # Replace with the actual path to your real video

# Define the paths for the output directories where the frames will be saved
fake_image_path_for_frame = 'output/fake_frames' # Replace with the desired output path for fake video frames
real_image_path_for_frame = 'output/real_frames' # Replace with the desired output path for real video frames

# Ensure the output directories exist
os.makedirs(fake_image_path_for_frame, exist_ok=True)
os.makedirs(real_image_path_for_frame, exist_ok=True)


extract_multiple_videos(fake_video_name, fake_image_path_for_frame)
extract_multiple_videos(real_video_name, real_image_path_for_frame)

from skimage import measure
def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
# return the MSE, the lower the error, the more "similar"
    # the two images are
    return err
def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = measure.compare_ssim(imageA, imageB)
    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap = plt.cm.gray)
    plt.axis("off")
    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap = plt.cm.gray)
    plt.axis("off")
    # show the images
    plt.show()
