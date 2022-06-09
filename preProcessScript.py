import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process image path.')
    parser.add_argument('--path', help='path of the image')
    args = parser.parse_args()
    print(args.path)

    img = cv2.imread(args.path, 0)
    
    #im2double
    quanta = 20
    maximum = img.flatten().max()
    img = img / maximum
    #GaussBlur
    # img = cv2.GaussianBlur(img,(3,3),0)
    #Quanta
    img = img * quanta
    img = img.round()
    img = img / quanta * maximum

    thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    dilation = cv2.dilate(thresh,kernel,iterations = 1)

    img = cv2.resize(img, (500, 800))
    thresh = cv2.resize(thresh, (500, 800))
    opening = cv2.resize(opening, (500, 800))
    dilation = cv2.resize(dilation, (500, 800))

    # cv2.imshow('image',(~thresh.astype(np.uint8))) 
    cv2.imshow('image',(opening.astype(np.uint8))) 
    cv2.waitKey()
    cv2.destroyAllWindows()
    