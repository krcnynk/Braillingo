import pytesseract
from pytesseract import Output
import cv2
import argparse
import numpy as np
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process image path.')
	parser.add_argument('--path', help='path of the image')
	args = parser.parse_args()
	img = cv2.imread(args.path,0)
	img = cv2.equalizeHist(img)
	d = pytesseract.image_to_data(img, output_type=Output.DICT)
	n_boxes = len(d['level'])
	for i in range(n_boxes):
	    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
	    crop_img = img[y:y+h, x:x+w]
	    if int(d['conf'][i]) != -1:
		    cv2.imwrite('./croppedParts/' + str(i) +'_'+str(d['conf'][i])+'.jpg',crop_img)
		    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

	_, thresholded = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,21,10)
	cv2.imshow('img', thresholded)
	cv2.waitKey(0)
	if np.mean(thresholded) > 127:
		cv2.bitwise_not(thresholded)
	#blur_weight = 7
	#img_blurred = cv2.medianBlur(thresholded, blur_weight)
	img_blurred = cv2.GaussianBlur(thresholded,(3,3),0)
	dilated = cv2.dilate(img_blurred, kernel=np.ones((3, 3), np.uint8))
	#cv2.imshow('img', img)
