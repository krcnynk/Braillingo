import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import argparse
import matplotlib.pyplot as plt

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
    
def getNspacing(rows,N):
	np.intc()
	minrowIndexMGS = np.min(rows)
	maxrowIndexMGS = np.max(rows)
	spacing = (maxrowIndexMGS-minrowIndexMGS)/N;
	rowNumbers = []
	for i in range(0,N):
		rowNumbers.append(find_nearest(rows, maxrowIndexMGS-spacing*i))
	#print(rows,rowNumbers)
	return rowNumbers

def drawLines(img,spacedRows):
	
	for a in spacedRows:
		start_point = (0, a)
		end_point = (img.shape[1], a)
		color = (0, 255, 0)
		thickness = 1
		img = cv2.line(img, start_point,end_point, color, thickness) 
		
	cv2.imshow('image',img) 
	cv2.waitKey()
	cv2.destroyAllWindows()
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process image path.')
	parser.add_argument('--path', help='path of the image')
	args = parser.parse_args()
	print(args.path)

	img = cv2.imread(args.path,0)
	img = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
	horizontalDimSum = np.sum(img,axis=1)
	hist, bin_edges = np.histogram(horizontalDimSum)
	maximumGrayscaleSum = np.max(horizontalDimSum)
	minimumGrayscaleSum = np.min(horizontalDimSum)
	condition = 10*(maximumGrayscaleSum-minimumGrayscaleSum)/11 + minimumGrayscaleSum
	#rowIndexsMGS = np.where(horizontalDimSum > condition)
	rowIndexsMGS = np.argpartition(horizontalDimSum, -50)[-50:]
	print(np.max(horizontalDimSum),horizontalDimSum.shape,condition)
	print(rowIndexsMGS[0])
	#plt.plot(bin_edges[:-1], hist)
	#plt.xlim(min(bin_edges), max(bin_edges))
	#plt.show()  
	spacedRows = getNspacing(rowIndexsMGS[0],10)
	drawLines(img,spacedRows)
    
