from tools import tileIndex
from tools import indexToRowCol

def testTileIndex():
	success = True
	success = (success and (tileIndex(45.795,4.7702)==0))
	success = (success and (tileIndex(45.695,4.7702)==-1))
	success = (success and (tileIndex(45.705,4.7702)==90))
	success = (success and (tileIndex(45.705,4.7695)==-1))
	success = (success and (tileIndex(45.74059,4.8002)==53))
	success = (success and (tileIndex(45.74059,4.8702)==-1))
	return success

def testIndexToRowCol():
	success=True
	success=(success and (indexToRowCol(12)==[1,2]))
	success=(success and (indexToRowCol(0)==[0,0]))
	success=(success and (indexToRowCol(100)==-1))
	success=(success and (indexToRowCol(99)==[9,9]))
	return success

print(testTileIndex())
print(testIndexToRowCol())
