#current as of 8/8/13
#most recent changes:
#general cleanup
#AFTER the first TESTING EDITION -> scratched that since cylinder wasn't showing up (accidentally put invisible in visibleArrowCylinder())
#ideas include: making an average leg angle for left and right legs
# to reduce jumps in trackers resulting in steps
#compare angles of both feet between trackers. Match angle closest to the other (see sortAngle).
# If the difference is greater than (45?) degrees, the one of the kinects is freaking out so do not
# change anything (either start or stop moving).
#using a system similar to Wendt et al. where we measure how fast foot position
# (could we use angle instead?) changes. move person forward based on difference
# between current leg angle and last leg angle. make sure that leg angle is greater
# than threshold so we don't move incredibly small amounts when standing still?
# also need to make sure that our turning algorithm is super bueno. Or maybe the difference has to be
# greater than a certain threshold. We could use exponential function or polynomial so that the greater
# the difference, the faster/farther the person moves. We could also say that if the difference was greater
# than a really big threshold, to disregard it, like for jumps. Have a boolean for positive, so random
# decreases in angles won't cause strangeness. But at the same time, the foot has to come back down.
# So the boolean for positive does not seem like such a good idea

import viz
import viztask
import vizjoy
import vizinfo
import vizshape
import vizact
import os
import math
import random
import datetime
import time
import linecache

#Brings up menu for HMD etc.
viz.go(viz.PROMPT)
# Get and validate a subject ID
test = True
sight = test
validID = False
while not (validID):
  try:
		#Prompt the user for an ID number
		subjectID = int(viz.input('Input Subject ID Number'))
		RESULTS_DIRECTORY = 'C:\Users\Administrator\Downloads'
		#Validate the subject ID number
		outFilePath = '%s\Subject_%s.txt' %(RESULTS_DIRECTORY, str(subjectID))
		if os.path.exists(outFilePath) or subjectID is '':
			yes = viz.ask('The Subject ID Number ' + str(subjectID) + ' already exists. Pick a new one?')
			if not yes:
				raise 'Exiting...'
		else:
			validID = True
			print "we have a valid ide!"
	except ValueError:
		print('Subject ID number must be an integer')
if test:
	subjectInitial = 'test'
else:
	subjectInitial = (viz.input('Input subject inital'))
#Determine whether or not trial recording is enabled 
#recordingEnabled = viz.get(viz.OPTION2)
recordingEnabled = not test
#print recordingEnabled
if recordingEnabled:
	print "we are recorders!"
	dirPath = './Results/Subject_%s' % (str(subjectID))
	if(not os.path.exists(dirPath)):
		print "making directory!"
		os.makedirs(dirPath)
	recordFile = open('Results\Subject_%s\Research2013_%s.txt ' % (str(subjectID), subjectInitial), 'w')
	
debugPath = './AfterTestTesting'
if (not os.path.exists(debugPath)):
	os.makedirs(debugPath)
debugFile = open(debugPath + '/test%s.txt'%(str(subjectID)), 'w')
##################Get height###############################
if test:
	PART_HEIGHT = 2
else:
	PART_HEIGHT=viz.input("Enter Subject Height in Meters:")
	recordFile.write('Height:'+ str(PART_HEIGHT) + '\n')
	recordFile.write('Object,Object Name,StartX,StartY,StartZ,Start Angle,Angle Turned,Angle Needed,Time,turningerror,movedwhileTurning\n')
HEIGHT_TO_STRIDE = .414
strideLength = 1
print "strideLength = %f" %strideLength
tracker = viz.add('intersense.dls')
''' *************************** KINECT CODE ***************************** '''
#myHead = vrpn.addTracker( 'Tracker0@localhost', HEAD)
HEAD = 0
NECK = 1
TORSO = 2
WAIST = 3
LEFTCOLLAR = 4
LEFTSHOULDER = 5
LEFTELBOW = 6
LEFTWRIST = 7
LEFTHAND = 8
LEFTFINGERTIP = 9
RIGHTCOLLAR = 10 
RIGHTSHOULDER = 11
RIGHTELBOW = 12
RIGHTWRIST = 13
RIGHTHAND = 14
RIGHTFINGERTIP = 15
LEFTHIP = 16
LEFTKNEE = 17
LEFTANKLE = 18
LEFTFOOT = 19
RIGHTHIP = 20
RIGHTKNEE = 21
RIGHTANKLE = 22
RIGHTFOOT = 23

# Store trackers, links, and vizshape objects
trackers = []
trackersB = []
trueTrackers = []

# Start vrpn
vrpn = viz.addExtension('vrpn7.dle')
#desktop
trackerLocationA = 'Tracker0@10.10.38.160'
#laptop
trackerLocationB = 'Tracker0@10.10.35.180'

for i in range (24):
	trackers.append(vrpn.addTracker(trackerLocationA,i))
	trackersB.append(vrpn.addTracker(trackerLocationB,i))
trueTrackers = trackers

#######################view stuff######################
view = viz.MainView
view.collision(viz.OFF)
viz.eyeheight(PART_HEIGHT)
view.setPosition(0,PART_HEIGHT,0)
viz.link(tracker, view)

#########################step stuff########################
foot = False		#false left foot, true right foot, mostly used for debugging
aIsTrue = False
RIDICULOUS = 56
###################gaze angle stuff#######################
finalYaw = 0
previousYaw = 0
turning = 0
stepCount = 0
########################foot angle stuff#####################
aveFootAngle1 = 0
aveFootAngle2 = 0
footAngle1 = []
footAngle2 = []
FOOTANGLEARRAYLENGTH = 10
####################different file stuff#####################
comp = 2
if comp == 1:		#we are using the laptop
	commonAddress = 'C:\\Users\\prestontunnellwilson\\Downloads\\Research2013\\Viz4Obj\\'
elif comp == 2:		#we are using betsy's laptop
	commonAddress = 'C:\\Users\\Williams\\Downloads\\Objects\\'
else:
	commonAddress = 'C:\\Users\\Administrator\\Downloads\\Objects\\'
	
#################reading in file stuff###################
#Targetfile = open('targetobjectorder.txt', 'r')    # opens target order
#Conditionfile = open('conditionorder.txt','r') #opens condition order


"""******************Addresses******************"""
#could use a for loop, have an array for the specific filles and a
#string for the ending. then we could just display the name of the target
ojbectEnding = '.WRL'
#address 0
dogAddress =  'THEREALDOG'
chairAddress =  'thechair'
barrelAddress =  'THEBARREL'
birdAddress =  'thebirds'
plantAddress =  'plant'
shieldAddress =  'shield'
#address 1
bookshelfAddress =  'bookshelf'
harpAddress =  'HARP'
chaliceAddress =  'THECHALICE'
clockAddress =  'THECLOCK'
crateAddress =  'THEBOX'
phoneboothAddress =  'THEPHONEBOOTH'
#address 2
piggybankAddress =  'THEPIGGYBANK'
treasurechestAddress =  'THETREASURECHEST'
urnAddress =  'THEURN'
washingmachineAddress =  'THEWASHINGMACHINE'
watchAddress =  'watch'
wheelbarrowAddress =  'wheelbarrow' #this file name is wheelbarrow.ive

"""*****************************************************"""

addresses0 = [dogAddress, chairAddress, barrelAddress, birdAddress, plantAddress, shieldAddress]
addresses1 = [bookshelfAddress, harpAddress, chaliceAddress,clockAddress, crateAddress,phoneboothAddress]
addresses2 = [piggybankAddress, treasurechestAddress,urnAddress,washingmachineAddress,watchAddress, wheelbarrowAddress]
#contains the objects pointed to in addresses

slopefromthreeto5 = .7718232131
xdif = .5
objects = []
objectAddresses = [addresses0,addresses1, addresses2]
objectFiles = []

objectHeight = 0
#Create locations for all of the objects in the envirnoment
masterObjectLocations = [[-1.04082, objectHeight, 24],
	[-8.44218,objectHeight, 4.5714],
	[-15.2653,objectHeight, -9.90476],
	[1.04082,objectHeight, -11.8095],
	[12.6054,objectHeight, -21.7143],
	[15.6122 + xdif,objectHeight, -9.71429 + xdif * slopefromthreeto5]]

dojo = viz.addChild("ground_grass.osgb")
dojo.setScale(1.5,1.5,1.5)
sky = viz.addChild("sky_day.osgb")

#Add a joystick
joystick = vizjoy.add()

objectSet = 0

testingHeight = 0
#positions of cylinders for people to walk to and use to orient selves
masterTargetLocations = [[-17, testingHeight, 1.3333],
	[-7.17007, testingHeight, -11.2381],
	[1.04082, testingHeight, -23.8095],
	[8.21088, testingHeight, -15.619],
	[6.82313, testingHeight, -3.80952],
	[15.2653, testingHeight, 2.47619]]
targetLocations = []
#positions of arrows for people to face towards
offset = 2
fournegrecslope = -.7224
arrowHeight = 1.5
masterArrowLocations = [[masterTargetLocations[0][0], arrowHeight, masterTargetLocations[0][2] + offset],
	[masterTargetLocations[1][0] + math.cos(math.pi / 4.25) * offset, arrowHeight, masterTargetLocations[1][2] + math.sin(math.pi / 4.25) * offset],
	[masterTargetLocations[2][0] + offset, arrowHeight, masterTargetLocations[2][2]],
	[masterTargetLocations[3][0], arrowHeight, masterTargetLocations[3][2] - offset],
	[masterTargetLocations[4][0] - offset, arrowHeight, masterTargetLocations[4][2] - fournegrecslope * offset],
	[masterTargetLocations[5][0] - offset, arrowHeight, masterTargetLocations[5][2]]]


fileStartIndex = 0
#how much to rotate each target: target0 is rotated 45 degrees with each rotation
targetRotations = [45, 180, 30, 310, 100, 350]
angleIndex = 0

#from each spot corresponding to index in list, turn to these targets
#note that these are not randomized yet
masterTargetObjects = [[0,1,2],
	[0,2,3],
	[2,3,5],
	[3,4,5],
	[0,3,5],
	[0,4,5]]
targetObjects = []
targetPosition = [0,0,0]
#order in which to call the objects at the testing locations
#make sure that len(targetObjectsOrder) % len(targetObjects) == 0
#	and len(targetObjectsOrder) % len(targetObjects[0]) == 0
#NOTE: this is the order for the corresponding set for masterTargetObjects
#	ie, if the sixth set is first, the sixth set of the current targetOrder
#	would be used, not the first set
targetOrder = [[1,2,0, 2,0,1, 2,0,1, 1,2,0, 2,0,1, 2,0,1],
	[2,1,0, 2,1,0, 0,2,1, 0,2,1, 0,1,2, 0,2,1],
	[0,1,2, 0,1,2, 0,1,2, 0,1,2, 0,1,2, 0,1,2]]

#order in which to go to testing locations
#	where locationCounter is incremented each time a location is finished (all 3 objects are called)
#	and targetCounter incrementes after each target
locationOrder = [[1,4,2,3,5,0],
	[5,4,3,0,2,1],
	[0,1,2,3,4,5]]

#reset targetCounter and locationCounter after a condition is finished
targetCounter = 0		#keeps track of which index to use in targetObjects
locationCounter = 0		#keeps track of which testing location to use

condition = [0,1,2]		#order in which to do conditions: 0-joystick, 1-wip, 2-wipscaled
currentCondition = 0	#keeps track of current condition; also used in locationOrder[conditionCounter][locationCounter]

#to call something in targetObjects:
#targetObjects[locationOrder[conditionCounter][locationCounter]][targerOrder[conditionCounter][targetCounter]]

currentTarget = 0
rotation = 0

#angle target starts out facing and angle target turns to
turnAngle = 0
startAngle = 0

startTime = time.clock()

#amount of rounds completed. once fifteen is reached, new condition
testsCompleted = 0

#0-observe,1-walk,2-turn,3-reorient
currentState = 0
locationFinished = False

cylinder = viz.add('cylinder.wrl')
cylinder.setPosition(masterTargetLocations[0])
cylinderScale = (4,3,4)
cylinderTransparency = .5
cylinder.setScale(cylinderScale)
cylinder.alpha(cylinderTransparency)
cylinder.visible(viz.OFF)

arrow = viz.add('arrow.wrl')
#arrow.setScale(0.05, 0.3, 0.05)
arrow.setPosition(0,0.7,0.25)
arrow.alpha(0.8)
arrow.visible(viz.OFF)

#############################File Functions###############
#reads the file locationOrder. it returns a big array that has 3 smaller arrays of 5 numbers
#should be used for LocationOrderObjects
def LocationOrder(fileName, lines = 1):
	MODerator = subjectID % 12 * lines
	list = []
	index = 0
	
	debug = False
	if debug:
		print MODerator
		print MODerator + lines
	
	MODerator +=1		#since line number starts with 1 instead of 0
	
	for number_index in range(MODerator, MODerator + lines):
		#print "inside for loop"
		if lines != 1:
			list.append([])
		
		real_line = linecache.getline(fileName, number_index)
		
		if real_line == '\n':
			real_line = linecache.getline(fileName, number_index+1)

		for character in real_line:
			#print "inside the other loop"
			if(character == ' '):
				pass
			elif(character == '\n'):
				pass
			else:
				if lines != 1:
					list[index].append(int(character))
				else:
					list.append(int(character))
				
		index += 1
		
	return list
	
#assigns variables read from LocationOrderReader, 
#ConditionOrderReader, and TargetOrderReader
def FileReader():
	global condition, targetOrder, locationOrder
	condition = LocationOrder("conditions.txt")
	targetOrder = LocationOrder("indexOrder.txt",3)
	locationOrder = LocationOrder("random.txt",3)
	
	debug = False
	if debug:
		print "starting debug"
		print condition
		print targetOrder
		print locationOrder
		
##################################################################
#*****************************Angle Functions**********************
def unitVector(x,y,z):
	vecMag = math.sqrt(x*x+y*y+z*z)
	return x/vecMag, y/vecMag, z/vecMag

# function that takes three positions and returns angle between AB and AC
def getAngle(A, B, C):
	if (A == B and B == C and C == (0,0,0)):
		return 0
	vectorAB = B[0] - A[0], B[1] - A[1], B[2] - A[2]
	vectorAC = C[0] - A[0], C[1] - A[1], C[2] - A[2]
	
	dot = dotProduct(vectorAB, vectorAC)
	magAB = magnitude(vectorAB)
	magAC = magnitude(vectorAC)
	try:
		theta = math.acos(dot / magAB / magAC)
	except ZeroDivisionError:
		return 0
	return math.degrees(theta)
	
def get2Angle(A, B, C):
	if (A == B and B == C and C == (0,0,0)):
		return 0
	vectorAB = B[0] - A[0], B[1] - A[1], B[2] - A[2]
	vectorAC = C[0] - A[0], C[1] - A[1], C[2] - A[2]
	
	dot = TwoDotProduct(vectorAB, vectorAC)
	magAB = TwoMagnitude(vectorAB)
	magAC = TwoMagnitude(vectorAC)
	try:
		theta = math.acos(dot / magAB / magAC)
	except ZeroDivisionError:
		return 0
	return math.degrees(theta)
	
#gets angle between two vectors
#as of 8/7/2013 not called
def getVAngle(vectA, vectB):
	if (vectA == vectB and vectB == (0,0,0)):
		return 0
	
	dot = dotProduct(vectA, vectB)
	magA = magnitude(vectA)
	magB = magnitude(vectB)
	
	try:
		theta = math.acos(dot / magA / magB)
	except ZeroDivisionError:
		return 0
	return math.degrees(theta)
	
#returns dot product disregarding y.
def TwoDotProduct(vectA, vectB):
	xA = vectA[0]
	zA = vectA[2]
	
	xB = vectB[0]
	zB = vectB[2]
	
	return xA*xB + zA*zB
	
#returns magnitude disregarding y
def TwoMagnitude(vect):
	x = vect[0]
	z = vect[2]
	return math.sqrt(x*x + z*z)	
	
#takes in a vector, returns magnitude of that vector
def magnitude(vect):
	x = vect[0]
	y = vect[1]
	z = vect[2]
	return math.sqrt(x*x + y*y + z*z)
	
	
#takes in two vectors, returns dot product of vectors
def dotProduct(vectA, vectB):
	xA = vectA[0]
	yA = vectA[1]
	zA = vectA[2]
	
	xB = vectB[0]
	yB = vectB[1]
	zB = vectB[2]
	
	return xA*xB + yA*yB + zA*zB

#takes in three points and returns normal vector
#as of 8/7/2013 not called
def crossProduct(pA, pB, pC):
	x1 = pB[0] - pA[0]
	y1 = pB[1] - pA[1]
	z1 = pB[2] - pA[2]
	
	x2 = pC[0] - pA[0]
	y2 = pC[1] - pA[1]
	z2 = pC[2] - pA[2]
	
	return y1 * z2 - z1 * y2, x1 * z2 - x2 * z1, x1 * y2 - x2 * y1


#############################step detection and move functions###
def switchCam():
	global trueTrackers, aIsTrue
	global quadrant
	oldTracker = aIsTrue	
	debug = True
	
	distA = abs(trackers[RIGHTHIP].getPosition()[0] - trackers[LEFTHIP].getPosition()[0])
	distB = abs(trackersB[RIGHTHIP].getPosition()[0] - trackersB[LEFTHIP].getPosition()[0])
	
	if distA > distB:
		aIsTrue = True
		trueTrackers = trackers
	else:
		aIsTrue = False
		trueTrackers = trackersB
	
	if debug and oldTracker is not aIsTrue:
		print "we are using tracker A: ", aIsTrue
		
wait = True
def checkTurning():
	global previousYaw, previousTime, turning, wait
	
	angleThreshold = 3
	#if turning and wait then wait to update turning
	if turning and wait:
		wait = False
	#else either we are ready or we weren't turning
	else:
		turning = ((finalYaw < (previousYaw - angleThreshold)) or (finalYaw > (previousYaw + angleThreshold)))
		previousYaw = finalYaw
		wait = turning
	
def sortAngle(ang1, ang2, benchmark1, benchmark2):
	difangAbench1 = abs(benchmark1 - ang1)
	difangAbench2 = abs(benchmark2 - ang1)
	difangBbench1 = abs(benchmark1 - ang2)
	difangBbench2 = abs(benchmark2 - ang2)
	
	#if ang1 is best fit for bench1 and bench1's best fit is ang1
	return (difangAbench1 < difangBbench1 and difangAbench1 < difangAbench2)
	
def getAverage(array1):
	notStepping = 176.14159
	total = 0
	for x in array1:
		total += x
	try:
		ret = total / len(array1)
	except(ZeroDivisionError):
		#have to return a number bigger than threshold so we don't move
		return notStepping
	#I have not met someone who is so flexible that ze can do this
	if ret == 0:
		return notStepping
	#else we have actual data
	return ret

def updateFeetAngle(ang1, ang2):
	global aveFootAngle1, aveFootAngle2, footAngle1, footAngle2
	#if there is some sort of issue with tracking, return. We don't want zero's in here
	if ang1 == ang2 and ang2 == 0:
		return
	#if ang1 belongs with footAngle1
	if (sortAngle(ang1, ang2, aveFootAngle1, aveFootAngle2)):
		footAngle1.append(ang1)
		footAngle2.append(ang2)
	#else ang1 belongs with footAngle2
	else:
		footAngle1.append(ang2)
		footAngle2.append(ang1)
		
	if len(footAngle1) >= FOOTANGLEARRAYLENGTH:
		footAngle1.pop(0)
		footAngle2.pop(0)
		
	#update the averages
	aveFootAngle1 = getAverage(footAngle1)
	aveFootAngle2 = getAverage(footAngle2)

	
off = 11		#precise amount off
ERROR = (43- off) * -1	#AMOUNT OF DEGREES to correct movement
def step():
	global stepCount, finalYaw

	scalar = 1
	SCALED_CONDITION = 2
	TRANSLATE_SCALAR = 2		#how much to scale on physical step to
	if condition[currentCondition] == SCALED_CONDITION:
		scalar = TRANSLATE_SCALAR
	move(scalar)

	stepCount += 1
	print "here is stepcount: ", stepCount
	
	
moving = False
checkStepOut = ""
def checkStep():
	global finalYaw
	global foot
	global trueTrackers, turning
	global checkStepOut, moving
	JOYSTICK_CONDITION = 0
	if condition[currentCondition] == JOYSTICK_CONDITION:
		return
	
	finalYaw = tracker.getData()[3]
	# evaluate flag_outB if flag_side_cam is turned on
	switchCam()
	
	angleInfo = True
	#check to make sure data is accurate
	leftFootHeight = trueTrackers[LEFTANKLE].getPosition()[1]
	leftKneeHeight = trueTrackers[LEFTKNEE].getPosition()[1]
	leftHipHeight = trueTrackers[LEFTHIP].getPosition()[1]
	rightFootHeight = trueTrackers[RIGHTANKLE].getPosition()[1]
	rightKneeHeight = trueTrackers[RIGHTKNEE].getPosition()[1]
	rightHipHeight = trueTrackers[RIGHTHIP].getPosition()[1]

	
	if(leftFootHeight > leftHipHeight or rightFootHeight > rightHipHeight or leftFootHeight > leftKneeHeight or rightFootHeight > rightKneeHeight):
		return
		
	angleR = getAngle(trueTrackers[RIGHTKNEE].getPosition(), trueTrackers[RIGHTHIP].getPosition(), trueTrackers[RIGHTANKLE].getPosition())
	angleL = getAngle(trueTrackers[LEFTKNEE].getPosition(), trueTrackers[LEFTHIP].getPosition(), trueTrackers[LEFTANKLE].getPosition())
	
	updateFeetAngle(angleR, angleL)
	debug = False
	if debug:
		print aveFootAngle1
		print aveFootAngle2
	debugFile.write("ang1 " + str(footAngle1) + "\n")
	debugFile.write("ang2 " + str(footAngle2) + "\n\n")
	#current as of 8/7/2013
	angleThreshold = 145
	
	printangle = False
	if printangle:
		print "this is the right angle", angleR
		print "this is the left angle", angleL
		
	
	stepInfo = True

	bigAngle = 165
	
	if  moving and ((aveFootAngle1 >= bigAngle and aveFootAngle2 >= bigAngle) or turning):
		moving = False
		view.velocity(0,0,0)
		
	if not moving and (aveFootAngle1 < angleThreshold or aveFootAngle2 < angleThreshold) and not turning:
		if stepInfo:
			out = 'STEPPING!STEPPING!STEPPING!STEPPING!'
			if debug:
				print "we are using tracker A: ",aIsTrue
				print "we are stepping with right foot: ",foot
				print "this is the angle: ",angleL, angleR
		moving = True

	#continue to move if we are moving	
	if moving:
		step()
		foot = not foot
		if stepInfo:
			out = checkStepOut
	#else print why we weren't moving	
	else:
		if stepInfo:
			if angleL > angleThreshold or angleR > angleThreshold:
				if foot:
					out = "right foot "
				else:
					out = "left foot "
				out += "was not high enough"
			elif turning:
				out = "you were turning!"
			else:
				out = "how did you get here???"
	#print out what happened
	
	if stepInfo and out != checkStepOut:
		checkStepOut = out
		print checkStepOut

	
pause = False
def move(scale = 1):
	if pause:
		return
	data = tracker.getData()
	alpha =data[3]  + ERROR		#adding 45 degrees seems to correct direction
	
	x,y,z = unitVector(math.sin(math.radians(alpha)), 0, math.cos(math.radians(alpha)))
	
	x0, y0, z0 = viz.MainView.getPosition()
	#mode can be viz.speed or viz.time. value is the arg before it
	#if mode == time, value is amount of time it takes
	#if mode == speed, value is velocity to move
	#maybe wouldn't need error if set ori_mask to viz.HEAD_ORI
	update = vizact.goto([x*strideLength*scale+x0, y0, z*strideLength*scale+z0], 2, mode = viz.SPEED, ori_mask = viz.BODY_ORI)
	
	viz.MainView.runAction(update)
	#viz.MainView.velocity(0,0,0)
"""******************joystick functions*********"""		
def UpdateJoystick():
	global view
	y_threshold = 0.2

	#Get the joystick position
	x,y,z = joystick.getPosition()



	
	#Move the viewpoint forward/backward based on y-axis value
	if y < -y_threshold: 
	#	viz.MainView.move(x0*translateScalar,0,z0 * translateScalar,viz.BODY_ORI)
		#trying to move similarly to step
		move()


		
#UpdateJoystick every frame
def checkOption1():
	JOYSTICK_CONDITION = 0
	if condition[currentCondition] == JOYSTICK_CONDITION:
		#print "before first ontimer"
		UpdateJoystick()
		#print "after first ontimer"
		
#--------------------------------------------------------------	
#this function rotates the position of the objects by the
#given amount around the origin
#--------------------------------------------------------------
def rotate(angle, positions):
	
	#find the rotation matrix for the given angle
	radians = math.radians(angle)
	rotation = [[math.cos(radians), -math.sin(radians)], [math.sin(radians), math.cos(radians)]]
	
	
	newLocation = []
	#multiply all the locations by the matrix
	for x in range(len(positions)):
		newX = positions[x][0] * rotation[0][0] + positions[x][2] * rotation[0][1]
		newY = positions[x][0] * rotation[1][0] + positions[x][2] * rotation[1][1]
		newLocation.append([newX, positions[x][1], newY])
		
	return newLocation

#--------------------------------------------------------------
#this function roatates the objects about the dojo
#watch out for non-square coordinate environments. something to think about
#as of 8/7/2013, not used
#--------------------------------------------------------------
def rotateObjects(angle):
#	global rotation, objectLocations, objects
#	rotation = (rotation + angle) % 360
#	newPositions = rotate(rotation, objectLocations)
#	for x in range(len(newPositions)):
#		objects[x].setPosition(newPositions[x])
	dojo.setAxisAngle([0,1,0, angle], viz.REL_LOCAL)
	invisibleArrowCylinder()
	
	for x in range(len(objects)):
		temp_angle = objects[x].getEuler()[0]
		temp_angle += targetRotations[x]
		objects[x].setEuler(temp_angle,0,0)
	#myMessage = Message('Objects rotated to %d degrees' % rotation, 1)
	#viztask.schedule(myMessage.display())
	

#--------------------------------------------------------------
#this function changes the objects on the pillar
#as of 8/7/2013, not used
#we switch objects between positions, so unnecessary. Also, failing
# to account for how objects have moved when the prompt "please turn to face".
# Keeping track of a simple offset would fix the problem, but still, it would
# be unnecessary.
#--------------------------------------------------------------
def moveObjects(indexAmount):
	global objects, objectFiles, objectSet
	
	#loop through all of the pillars and delete their children and replace them with the new object
	for x in range(len(objects)):
		
		objects[x].setPosition(objectLocations[(indexAmount + x) % len(objectFiles[objectSet])])
		
#------------------------------------
#this function switches out the set of objects used
#-----------------------------------------------------
def changeObjects():
	global fileStartIndex, objects, objectFiles, objectSet
	debug = False
	objectSet = (objectSet + 1) % len(objectFiles)
	if debug:
		print "here is len(objects): %d" %len(objects)
	for x in range(len(objects)):
		temp = objectFiles[objectSet][x]
		temp.setPosition(objects[x].getPosition())
		objects[x].visible(viz.OFF)
		temp.visible(viz.ON)
		objects[x] = temp
		
#sets order in which to go to testing locations and in which order to call objects for each
# testing location
def getCurrentTestingLocationOrder():
	global targetLocations
	global arrowLocations
	global targetObjects
	
	debug = False
	info = True
	targetLocations = []
	arrowLocations = []
	targetObjects = []
	
	currentLocationOrder = locationOrder[currentCondition]
	if debug:
		print "currentLocationOrder",currentLocationOrder
	for i in range(len(masterTargetObjects)):
		arrowLocations.append([])
		targetLocations.append([])
		targetObjects.append([])
		
		currentTargetObjectIndex = currentLocationOrder[i]
		currentTargetObject = masterTargetObjects[currentTargetObjectIndex]
		if debug:
			print currentTargetObject
			print currentTargetObjectIndex
		for j in range(len(masterTargetObjects[i])):
			indexTargetOrder = currentTargetObjectIndex * len(currentTargetObject) + j
			nextObjectIndex = targetOrder[currentCondition][indexTargetOrder]
			if debug:
				print indexTargetOrder
				print nextObjectIndex
			targetLocations[i].append(masterTargetLocations[locationOrder[currentCondition][i]][j])
			arrowLocations[i].append(masterArrowLocations[locationOrder[currentCondition][i]][j])
			targetObjects[i].append(currentTargetObject[nextObjectIndex])
	if debug:
		print targetLocations
		print arrowLocations
		print targetObjects
		
	if info:
		print targetObjects
		print locationOrder[currentCondition]
		printOrderObjects()
		
def changeConditions():
	global currentState, targetToFace, fileStartIndex, currentTarget
	global targetToFace, view, currentCondition
	
	keyEvent('h')
	keyEvent('o')
	#keyEvent('r')
	#keyEvent('m')
	
	currentTarget = fileStartIndex = 0
	currentState = targetToFace = 0
	changeState(currentState)

	view.setPosition(0,PART_HEIGHT,0)
	
	angleArray = [45,90,45]
	#currentviewYaw = view.getEuler()[0]
	hackoffset = 0
	if (angleIndex == 1):
		hackoffset = 45
	view.setEuler(angleArray[angleIndex] + hackoffset,0,0)
	
	currentCondition += 1
	if currentCondition > 2:
		print "finished with testing!"
		currentCondition %= 3
	getCurrentTestingLocationOrder()
		
#makes things visible or not
def visibleScenery():
	global dojo, sky
	dojo.visible(viz.ON)
	sky.visible(viz.ON)
def invisibleScenery():
	global dojo, sky
	dojo.visible(viz.OFF)
	sky.visible(viz.OFF)
def visibleArrowCylinder():
	global cylinder, arrow
	arrow.visible(viz.ON)
	cylinder.visible(viz.ON)
def invisibleArrowCylinder():
	global cylinder, arrow
	arrow.visible(viz.OFF)
	cylinder.visible(viz.OFF)
	
#--------------------------------------------------------------
#this function updates the scene to correspond with the given
#state of the experiment
#--------------------------------------------------------------
def changeState(state):
	global objects, objectLocations, targetLocations, targetRotations, currentTarget, rotation, startPosition, objectSet
	global cylinder, arrow, targetToFace, objectFiles, startFileIndex, targetObjects, targetPosition, startAngle
	global recordFile, angleIndex
	#print 'Changing state to: %d' % state
	debug = False
	#--------------------------------------------------------------
	#A state of 0 corresponds to showing all of the objects and no target
	if(state == 0):
		if recordingEnabled:
			recordFile.write('currentCondition: %d\n' %condition[currentCondition])
		visibleScenery()
		keyEvent('s')
		invisibleArrowCylinder()
	
	#--------------------------------------------------------------
	#A state of 1 corresponds to showing the target and waiting for the participant to
	#walk toward the target and face the right direction
	elif(state == 1):
		if debug:
			print 'Target Number: %d' % currentTarget
			#Calculate the position of the cylinder
			print targetLocations
		targetPosition = rotate(rotation, targetLocations)[currentTarget]
		targetRotation = targetRotations[currentTarget] + rotation
		cylinder.setPosition(targetPosition)
		
		angleArray = [45,90,45]
		#Calculate the position of the arrow
		#arrowZ = targetPosition[0] + 1 * math.sin(math.radians(targetRotation + rotation))
		#arrowX = targetPosition[2] + 1 * math.cos(math.radians(targetRotation + rotation))
		#arrow.setPosition(arrowX, arrow.getPosition()[1], arrowZ)
		arrowPosition = rotate(rotation, arrowLocations)[currentTarget]
		arrow.setPosition(arrowPosition)
		cylinder.setEuler(targetRotation)
		
		#show all of the objects and the cylinder and the arrow
		visibleScenery()
		keyEvent('s')
		visibleArrowCylinder()
		if debug:
			print "arrow should be on"
		
	#--------------------------------------------------------------
	#A state of 2 corresponds to hiding the scene and waiting for the
	#participant to finish turning
	elif(state == 2):
		global startTime
		if not sight:
			invisibleScenery()
			keyEvent('h')
		invisibleArrowCylinder()
		startPosition = view.getPosition()
		startAngle = view.getEuler()[0] + ERROR
		startTime = time.clock()
		
		if debug:
			#this is a very important print statement
			print 'StartIndex: %d, Index: %d' % (fileStartIndex, (fileStartIndex + targetObjects[currentTarget][targetToFace]) % len(objectFiles[objectSet]))
		
		viztask.schedule(ShowMessage('Please turn to face %s' % objectAddresses[objectSet][(fileStartIndex + targetObjects[currentTarget][targetToFace]) % len(objectFiles[objectSet])]))
		
	#--------------------------------------------------------------
	#A state of 3 corresponds to showing only the cylinder and arrow
	#so that the participant can be reoriented to the starting position
	elif(state == 3):
		if not sight:
			invisibleScenery()
			keyEvent('h')
		visibleArrowCylinder()
		if debug:
			print "arrow should be on"
		
def ShowMessage(mystring):
	info = vizinfo.add(mystring)
	messagePos = (.5, .5)		#change if want message in dif spot
	info.translate(messagePos)
	yield viztask.waitTime(2)
	info.visible(0)
	
		
def printOrderObjects():
	for set in targetObjects:
		for obj in set:
			print objectAddresses[currentCondition][obj]
		
#as of 8/7/2013, never called
def objPos():
	global objects
	for x in range (len(objects)):
		print objects[x].getPosition()
	
def redoTrial(trial):
	global currentState, currentTarget, targetToFace, locationFinished
	
	#make arrows disappear and display objects
	currentState = 0
	
	#make arrow and cylinder position that of trial to redo
	currentTarget = trial
	
	#reset so that we start at the beginning again, it should be -1
	#no need to have it if set global currentState to 0
	#targetToFace = -1
	
	locationFinished = False
	
	changeState(currentState)

#--------------------------------------------------------------
#this function handles all of the keyboard input
#--------------------------------------------------------------
def keyEvent(key):
	global rotation, objectLocations, objects, cylinder, arrow, currentTarget, targetRotations, objectFiles, objectSet
	global startPosition, startAngle, targetPosition, pptLink, height, pptLink, recordingEnabled, recordFile
	global targetLocations, targetObjects
	global PART_HEIGHT
	global testsCompleted
	global fileStartIndex, angleIndex
	global example, horse, exapmleCylinder
	global locationFinished
	
	
	#print key
	#Rotate all of the objects in the scene
#	if(key == 'r'):
#		print 'YOU PRESSED R! WHAT ARE YOU DOING?'
#		angleArray = [45,90,45]
#		newPos = rotate(angleArray[angleIndex],targetLocations)
#		for ii in range(len(newPos)):
#			arrowPosition = rotate(angleArray[angleIndex], arrowLocations)[currentTarget]
#			arrow.setPosition(arrowPosition)
#			objects[ii].setPosition(newPos[ii])
#			
#		angleIndex = (angleIndex + 1) % len(angleArray)
		
	#Change the pillars the objects are on
#	elif(key == 'm'):
#		print "inside of m"
#		fileStartIndex = (fileStartIndex + 1) % len(objects)
#		moveObjects(fileStartIndex)
			
#	#Show the target to walk toward
#	elif(key == 't'):
#		global targetLocations, arrow
#		currentTarget = (currentTarget + 1) % len(targetLocations)
#		targetPosition = rotate(rotation, targetLocations)[currentTarget]
#		targetRotation = targetRotations[currentTarget] + rotation
#		cylinder.setPosition(targetPosition)
#		arrowX = targetPosition[0] + 0.3 * math.cos(math.radians(targetRotation + rotation))
#		arrowZ = targetPosition[2] + 0.3 * math.sin(math.radians(targetRotation + rotation))
#		#arrow.setPosition(arrowX, arrow.getPosition()[1], arrowZ)
#		arrow.setPosition([-9.873720169067383, 0.5, 3.1146695613861084])
#		cylinder.setEuler(targetRotations[currentTarget] + rotation)
#		cylinder.visible(viz.ON)
#		arrow.visible(viz.ON)
#	

	#hide the objects
	if(key == 'h'):
		for x in range (len(objects)):
			objects[x].visible(viz.OFF)
			
	#show the objects
	elif(key == 's'):
		for x in range (len(objects)):
			objects[x].visible(viz.ON)
			
	#switch the set of objects
	elif(key == 'o'):
		print"inside of o"
		changeObjects()
	
	#when a condition is done, push the almighty button
	elif(key == 'a'):
		changeConditions()

	#update the state
	elif(key == ' '):
		global  currentState, targetToFace, targetObjects, turnAngle
		
		debug = False
		if debug:
			print "current view angle: ", view.getEuler()[0] + ERROR
			print currentState
		#Show the next target to walk toward
		if(currentState == 0):
			currentState = 1
			if(recordingEnabled):
				recordFile.write('Target: %d\n' % currentTarget)
			changeState(currentState)
		#Hide the scene and let the participant turn
		elif(currentState == 1):
			targetToFace = -1
			currentState = 3
			#print 'Object Index: %d, Total Objects: %d' % (targetToFace, len(targetObjects[currentTarget]))
			changeState(currentState)
		#Show the arrow to reorient the participant
		elif(currentState == 2):
			global startTime
			timeDifference = time.clock() - startTime
			currentPosition = view.getPosition()
			movedTurned = False
			if startPosition != currentPosition:
				print "WARNING! STARTPOSITION IS NOT CURRENTPOSITION"
				movedTurned = True
				print startPosition
				print view.getPosition()
			#calculate the angle turned and the angle desired
			objectPosition = rotate(rotation, masterObjectLocations)
			objectNumber = targetObjects[currentTarget][targetToFace]
			destX = objectPosition[targetObjects[currentTarget][targetToFace]][0] - startPosition[0]
			destY = objectPosition[targetObjects[currentTarget][targetToFace]][2] - startPosition[2]
			mag = math.sqrt(destX*destX + destY*destY)
			normX = destX / mag
			normY = destY / mag
			startY = math.cos(math.radians(startAngle))
			startX = math.sin(math.radians(startAngle))
			endY = math.cos(math.radians(view.getEuler()[0] + ERROR))
			endX = math.sin(math.radians(view.getEuler()[0] + ERROR))
			dotNeeded = normX * startX + normY * startY
			dotTurned = startX * endX + startY * endY
			angleNeeded = math.degrees(math.acos(dotNeeded))
			angleTurned = math.degrees(math.acos(dotTurned))
			
			#print 'StartX: %f, StartY: %f, DestX: %f, DestY: %f, EndX: %f, EndY: %f' % (startX, startY, destX, destY, endX, endY)
			print 'Angle Needed: %f, Angle Turned: %f' % (angleNeeded, angleTurned)
			
			#not used as of 8/7/2013. Used to show file reader where to get info
			#see mod360.py for a way to use number of commas instead
			delim1 = '$'
			delim2 = '^'
			
			if(recordingEnabled):
				recordFile.write('%d,%s,%f,%f,%f,%f,%f,%f,%s%f%s, %s%f%s, %s\n' % (objectNumber,
				objectAddresses[currentCondition][(fileStartIndex + targetObjects[currentTarget][targetToFace]) % len(objectFiles[objectSet])],
				startPosition[0],startPosition[1],startPosition[2],startAngle,angleTurned,angleNeeded,delim1,timeDifference,delim1,delim2,abs(angleNeeded - angleTurned),delim2,movedTurned))
			
			currentState = 3
			if(targetToFace + 1 >= len(targetObjects[currentTarget])):
				currentTarget = (currentTarget + 1) % len(targetObjects)
				locationFinished = True
			changeState(currentState)
		#Hide everything again and let the participant turn toward the new target
		elif(currentState == 3):
			if locationFinished:
				currentState = 0
				locationFinished = False
				changeState(currentState)
				
			targetToFace = targetToFace + 1
			if debug:
				print "here is target to face: ",targetToFace
			testsCompleted += 1
			#print 'here is testscompleted: %d' %testsCompleted
			#print 'here is len of amount of targets: %d' % len(targetObjects[currentTarget])
			#if not finished with round
			if(targetToFace < len(targetObjects[currentTarget])):
				currentState = 2
				if debug:
					print 'Object Index: %d, Total Objects: %d' % (targetToFace, len(targetObjects[currentTarget]))
			#move on to next rotation
			else:
				print "move onto next location!"
				currentState = 0
				
			changeState(currentState)
			
	elif key == 'p':
		global pause
		pause = not pause
		
	elif key == 'd':
		pos = view.getPosition()
		update = vizact.goto([pos[0], pos[1] -1, pos[2]], 2, mode = viz.SPEED, ori_mask = viz.BODY_ORI)
		viz.MainView.runAction(update)
		
	elif key == 'e':
		example = not example
		if example:
			keyEvent('h')
			horse.visible(viz.ON)
			exapmleCylinder.visible(viz.ON)
		else:
			keyEvent('s')
			horse.visible(viz.OFF)
			exapmleCylinder.visible(viz.OFF)
			
	#if trial was messed up, redo that trial afterwards by pressing the number corresponding to that trial
	elif key == '1' or key == '2' or key == '3' or key == '3' or key == '4' or key == '5' or key == '0':
		redoTrial(int(key))
		
	else:
		print view.getPosition()
		
#objects to be used in example
horse = viz.add('horse.wrl')
horse.setPosition(-2,0,2)
exapmleCylinder = viz.add('cylinder.wrl')
exapmleCylinder.alpha(cylinderTransparency)
exapmleCylinder.setScale(cylinderScale)
exapmleCylinder.color(1,0,0)
exapmleCylinder.setPosition(3, 0, 3)
"""/////////////////////////////////////////////////////////////////////////////////////"""
def initializeLocations():
	global objects
	

	for x in range(len(masterObjectLocations)):
		objects.append(objectFiles[objectSet][x])
		
		objects[x].setPosition(masterObjectLocations[x])
		objects[x].alpha = 0.0
		objects[x].visible(viz.ON)

def initializeObjectFiles():
	global objectFiles
	
	for i in range(len(objectAddresses)):
		objectFiles.append([])
		for j in range(len(objectAddresses[i])):
			#account for wheelbarro.ive ending
			tempending = ojbectEnding
			if (i == 2 and j == 5):
				tempending = '.ive'
			objectFiles[i].append(viz.add(commonAddress + objectAddresses[i][j] + tempending))
			objectFiles[i][j].visible(viz.OFF)

	
def update():
	global currentState, arrow, cylinder, view, targetRotations, rotation, objects
	global targetObjects, currentTarget, targetToFace, targetPosition
	if(currentState == 1 or currentState == 3):
		#see if the participant is close enough to the cylinder
		x = view.getPosition()[0] - targetPosition[0]
		y = view.getPosition()[2] - targetPosition[2]
		distSqrd = x*x + y*y
		radius = 1.2
		#print 'ViewX: %f, ViewY: %f, TarX: %f, TarY: %f, Dist: %f' % (view.getPosition()[0], view.getPosition()[2], targetLocations[currentTarget][0], targetLocations[currentTarget][2], distSqrd)
		if(distSqrd <= radius):
			cylinder.color(0,1,0)
			#find the angle between the participant's view and the arrow
			#might have to add error in angle needed...
			pointA = view.getPosition()[0] + math.sin(math.radians(view.getEuler()[0] + ERROR)),0,view.getPosition()[2] + math.cos(math.radians(view.getEuler()[0] + ERROR))
			angle = get2Angle(view.getPosition(), pointA, arrow.getPosition())
			#angle += ERROR
			debug = False
			if debug:
				print "here is angle %d " %angle
				print "here is pointA",pointA
				print "here is the yaw %d", view.getEuler()[0]
			#print 'Angle: %f, Object Angle: %f' % (angle, targetRotations[currentTarget] + rotation)
			#print 'X: %f, Y: %f' % (cylinder.getPosition()[0] + math.sin(math.radians(cylinder.getEuler()[0])), cylinder.getPosition()[2] + math.cos(math.radians(cylinder.getEuler()[0])) - view.getPosition()[2])
			if(angle <= 10.0):
				arrow.color(0,1,0)
			else:
				arrow.color(1,0,0)
		else:
			cylinder.color(1,0,0)
			arrow.color(1,0,0)

	elif example:
		global exapmleCylinder
		x = view.getPosition()[0] - exapmleCylinder.getPosition()[0]
		y = view.getPosition()[2] - exapmleCylinder.getPosition()[2]
		distsqrd = x*x + y*y
		if distsqrd <= .8:
			exapmleCylinder.color(0,1,0)
		else:
			exapmleCylinder.color(1,0,0)
FileReader()		
initializeObjectFiles()
initializeLocations()
getCurrentTestingLocationOrder()

debugInitialize = False
if debugInitialize:
	print targetLocations
	print targetObjects
example = False
keyEvent('e')
#rotate once
#keyEvent('r')	
view.setEuler(45,0,0)

vizact.ontimer(0, checkStep)	
vizact.ontimer(0, checkOption1)
vizact.ontimer(0.2, update)
vizact.ontimer(0.2,checkTurning)
viz.callback(viz.KEYBOARD_EVENT, keyEvent)
print "outside of all ontimers"
