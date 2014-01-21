TILE_HEIGHT = 0.01
TILE_WIDTH = 0.01
GRID_HEIGHT = 10
GRID_WIDTH = 10
O_LAT = 45.8
O_LONG = 4.77

#Input: 	GPS Coordinates of a point
#Output:	Index of the zone in which is the point 
def tileIndex(lat,long):
	if ((lat > O_LAT) or (lat < (O_LAT - GRID_HEIGHT*TILE_HEIGHT)) or (long < O_LONG) or (long > (O_LONG+TILE_WIDTH*GRID_WIDTH))):
		return -1
	lat_delta = abs(lat - O_LAT)
	long_delta = long - O_LONG
	row = lat_delta // TILE_HEIGHT
	col = long_delta // TILE_WIDTH
	return rowColToIndex(row,col)

#Input:		Index of a zone
#Output:	Position of the zone in the grid (row,column)
def indexToRowCol(index):
	if ((index >= GRID_WIDTH*GRID_HEIGHT) or (index<0)):
		return -1
	row = index // GRID_WIDTH
	col = index - GRID_WIDTH*row
	return [row,col]

#Input:		Position of a zone in the grid (row,column)
#Output:	Index of the zone
def rowColToIndex(row,col):
	index = row * GRID_WIDTH + col
	return index


#	Input:
#	-index: index of a zone
#	
#	Output: Finds the zones on a square around the input zone, with a radius value of depth
def zonePerimeter(index,depth):
	tab = indexToRowCol(index)
	if ((tab == -1)or(depth<=0)):
		return -1
	row = tab[0]
	col = tab[1]
	perimeter = []

	#Upper and bottom horizontal sides of the square
	for iRow in [row-depth,row+depth]:
		for iCol in range(col-depth, col+depth+1):
			if isValid(iRow,iCol):
				perimeter.append(rowColToIndex(iRow,iCol))

	#Left and right vertical sides of the square
	for iCol in [col-depth,col+depth]:
		for iRow in range(row-depth+1,row+depth):
			if isValid(iRow,iCol):
				perimeter.append(rowColToIndex(iRow,iCol))
	perimeter.sort()
	return perimeter

def isValid(row,col):
	return ((col>=0) and (col<GRID_WIDTH) and (row>=0) and (row<GRID_HEIGHT))
