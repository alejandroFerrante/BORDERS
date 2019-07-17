### EXTRACT DATA FROM ### http://opentopo.sdsc.edu/raster?opentopoID=OTSRTM.042013.4326.1 ###
## git pull |  git add .  && git commit -m "someMessage" && git push origin master ##
# use example: python borders.py splitImage sampleData.txt 2 2 out.png #
# use example: python borders.py splitImageBorders sampleData.txt 2 2 out.png #
# use example: python borders.py splitImagePoints sampleData.txt 2 2 out.png #


import matplotlib.pyplot as plt ####
from skimage import measure 	####
import cv2


from scipy.misc import toimage
import noise
import numpy as np
import sys

from graphics import * #apt-get install python-tk
from copy import copy
import time;
import random
from scipy.misc import imsave


#python borders.py hmdata.txt 1000 1000 500 500 sample.png
#python borders.py hmdata.txt 2250 1400 150 150 10 30 75 1 1


def getHeightmapFromFile( file, fromX, fromY, toX, toY , limit):
	
	sizeX = toX - fromX
	sizeY = toY - fromY

	#print("fromX "+str(fromX)+" , toX "+str(toX)+" sizeX "+str(sizeX)+" || fromY "+str(fromY)+" , toY "+str(toY)+" sizeY "+str(sizeY) )

	dimensions = (sizeX,sizeY)
	heightMap = np.zeros(dimensions)
	
	j = 0
	
	while (j < sizeY) and (j < len(file)):

		line = file[fromY+j].split(" ")
		line = line[fromX:]
		line = filter(lambda a: a != " ", line)
		line = filter(lambda a: a != "\n", line)

		i = 0
		ii = 0

		while (i < sizeX) and (i < len(line)):
			val = line[i].replace("\n" , "")
			

			try:
				val = int(val)
	
				if val > limit :
					heightMap[ii][j] = 255
				else:
					heightMap[ii][j] = 0
				ii += 1
			except:
				ii = ii
				

			i += 1

		j += 1
	
	return heightMap

def getEdgesAsPointsStringList(edges , innerSeparator , outerSeparator ):
	res = ""
	firstWriteOccured = False

	j = 0
	for x in edges :
		i = 0
		for t in x :

			if (t > 0):
				#print("reading <"+str(t)+"> on ("+str(i)+","+str(j)+")")
				new = str(i)+innerSeparator+str(j)
				if firstWriteOccured :
					res += outerSeparator + new
				else:
					res += new

				firstWriteOccured = True

			i += 1
		j += 1
	return res

def main():

	#for arg in sys.argv[1:] :
		#print(arg)

	mode   				= sys.argv[1:][0]

	if (mode == "splitImage") or (mode == "splitImageBorders") or (mode == "splitImagePoints") :

		filename   			= sys.argv[1:][1]
		amountOfColQuadrants 	= int(sys.argv[1:][2])
		amountOfRowQuadrants 	= int(sys.argv[1:][3])
		outputname 			= sys.argv[1:][4]
		
		file = open(filename, 'rb').readlines()
		
		#FIRST THREE ROWS MUST CONTAIN THIS DATA
		cols  =  int(file[0])
		rows  =  int(file[1])
		limit =  int(file[2])
	
		file = file[3:]
	

		iterationRowSize = rows // amountOfRowQuadrants
		rowReminder = rows % amountOfRowQuadrants
		

		iterationColumnSize = cols // amountOfColQuadrants
		colReminder =  cols % amountOfColQuadrants
			
		#print("rows: "+str(rows)+" iterationRowSize: "+str(iterationRowSize)+" rowReminder: "+str(rowReminder))
		#print("cols: "+str(cols)+" iterationColumnSize: "+str(iterationColumnSize)+" colReminder: "+str(colReminder))


		j = 0
		jindex = 0
		while j < amountOfRowQuadrants:
			i = 0
			iindex = 0
			while i < amountOfColQuadrants :
				
				toX = iindex+iterationColumnSize
				toY = jindex+iterationRowSize

				print("Quadrant ("+str(i)+"-"+str(j)+")  >> X["+str(iindex)+","+str(toX)+"] Y["+str(jindex)+","+str(toY)+"]")
				hmap = getHeightmapFromFile( file, iindex, jindex, toX - 1, toY - 1 , limit)
								
				outname = (outputname.split(".")[0])+"_"+str(i)+str(j)+"."+(outputname.split(".")[1])
				
				imsave(outname, hmap)	

				if(mode == "splitImageBorders") or (mode == "splitImagePoints") :
				
					im = cv2.imread(outname)
					edges = cv2.Canny(im,100,200)


					if(mode == "splitImageBorders") :
						outname1 = (outputname.split(".")[0])+"_"+str(i)+str(j)+"(BORDERS)."+(outputname.split(".")[1])
						imsave(outname1, edges)
					else:
						outname1 = (outputname.split(".")[0])+"_"+str(i)+str(j)+"(POINTS).txt"
						text_file = open(outname1, "w")
						stringPoints = getEdgesAsPointsStringList(edges , "," , ";")
						text_file.write(stringPoints)
						text_file.close()

				i += 1
				iindex += iterationColumnSize

							
			j += 1
			jindex += iterationRowSize


if __name__== "__main__":
  main()