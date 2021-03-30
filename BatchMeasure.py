import glob
import re
import cv2
import skimage.exposure
import pandas as pd
import os

location = "./part1/"

files = sorted([f for f in glob.glob(location+"/**", recursive = True) if re.search(r'(.*)\.(jpg|jpeg)$', f)])
print(files)

def blur_contrast_brightness_measure(imagePath):
    image = cv2.imread(imagePath)
    blur_measure = cv2.Laplacian(image, cv2.CV_64F).var()

    low_contrast = False
    threshold = 0
    while not low_contrast:
        threshold = round(threshold + 0.025, 3)
        low_contrast = skimage.exposure.is_low_contrast(image, fraction_threshold=threshold)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    return [round(blur_measure, 3), threshold, round(hsv[...,2].mean(),3)]

df = pd.DataFrame(columns = ['File_name', 'Blur_Measure', 'Contrast_Measure', 'Brightness_Measure'])
for i in range(0, len(files)):
    filec = files[i]
    measure = blur_contrast_brightness_measure(filec)
    print(measure)
    df = df.append(pd.Series([os.path.basename(filec)]+measure, index=df.columns), ignore_index = True)

df.to_csv("image_stats.csv", index = False)
