#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor , OUTPUT_B , OUTPUT_C , MoveTank , SpeedPercent
from time import sleep
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, UltrasonicSensor

drive = MoveTank(OUTPUT_B , OUTPUT_C)
cs = ColorSensor()
us = UltrasonicSensor()
ts = TouchSensor()
sound = Sound()

ts.mode = 'TOUCH'
us.mode = 'US-DIST-CM'

blackValue = 20
def moveForward(a = 10, b = 10, c = 0.20):
    drive.on_for_rotations(SpeedPercent(a), SpeedPercent(b), c)
def turning(a = 1.0, b =-1.0, c = 0.025):
    drive.on_for_rotations(SpeedPercent(a), SpeedPercent(b), c)
def pivotRight(c = 0.025):
    drive.on_for_rotations(SpeedPercent(5), SpeedPercent(0), c)
def pivotRight90(a = 20, b = 0, c = 1):
    drive.on_for_rotations(SpeedPercent(a), SpeedPercent(b), c)
def pivotLeft90():
    drive.on_for_rotations(SpeedPercent(0), SpeedPercent(15), 1)
def pivotRightReverse():
    drive.on_for_rotations(SpeedPercent(-5), SpeedPercent(0), 0.025)
def pivotLeft(c = 0.025):
    drive.on_for_rotations(SpeedPercent(0), SpeedPercent(5), c)
def pivotLeftReverse():
    drive.on_for_rotations(SpeedPercent(0), SpeedPercent(-5), 0.025)

# check to see if we the robot need to correct its course
def check():
    count = 0
    while (cs.value() <= blackValue):
        pivotRightReverse()
        count = count + 1
        sleep(0.1)
    for i in range(count):
        pivotRight()
        sleep(0.1)
    rightPiv = count
    count = 0
    while (cs.value() <= blackValue):
        pivotLeftReverse()
        count = count + 1
        sleep(0.1)
    for i in range(count):
        pivotLeft()
        sleep(0.1)
    leftPiv = count

    correctPiv = rightPiv - leftPiv
    return correctPiv

def checkLong():
    count = 0
    while (cs.value() <= blackValue):
        pivotRight()
        count = count + 1
        sleep(0.1)
    for i in range(count):
        pivotRightReverse()
        sleep(0.1)
    rightPiv = count
    count = 0
    while (cs.value() <= blackValue):
        pivotLeft()
        count = count + 1
        sleep(0.1)
    for i in range(count):
        pivotLeftReverse()
        sleep(0.1)
    leftPiv = count

    correctPiv = rightPiv - leftPiv
    return correctPiv

def correct(pivotValue):
    if (pivotValue > 0):
        move = [10, 10.75]
    elif (pivotValue < 0):
        move = [10.75, 10]
    else:
        move = [10, 10]
    return move

def correctLong(pivotValue2, b = 0.5):
    if (pivotValue2 > 0):
        move2 = [10 + b, 10]
    elif (pivotValue2 < 0):
        move2 = [10, 10 + b]
    else:
        move2 = [10, 10]
    return move2

def continuousBlack():
    if cs.value() <= blackValue:
        moveForward(c=0.1)
        if cs.value() <= blackValue:
            moveForward(c=-0.05)
            return True
        return False
    else:
        return False


cs.mode='COL-REFLECT'

#FIRST PHASE
moveForward(c = 0.4)
sleep(2)
pivotRight90()
sleep(2)
moveForward(a = -10, b = -10, c = 0.3)
sleep(1)
onBlack = True
blackTiles = 1
sound.beep()
move = [10, 10]
while True:
    if (cs.value() <= blackValue and onBlack == False):
        blackTiles = blackTiles + 1
        if(blackTiles < 3):
            onBlack = True
            sound.beep()
        elif(blackTiles == 7):
            onBlack = True
            moveForward(c=0.075)
            sound.beep()
            pivotValue = check()
            if (pivotValue > 0):
                turn(-1, 1)
            elif (pivotValue < 0):
                turn(1, -1)
            else:
                continue
        else:
            onBlack = True
            moveForward(c = 0.075)
            sound.beep()
            pivotValue = check()
            print(pivotValue)
            move = correct(pivotValue)
    elif (cs.value() <= blackValue):
        onBlack = True
    else:
        onBlack = False

    if (blackTiles >= 7):
        break

    moveForward(move[0], move[1])

sleep(2)
sound.beep()
#SECOND PHASE
moveForward(c = 0.3)
pivotRight90()
sleep(1)
moveForward(a = -10,b =-10,c = 0.2)
sleep(1)
pivotValue = check()
move = correctLong(pivotValue)


moveForward(a = move[0], b = move[1], c = 1.7)

onBlack = continuousBlack()

while onBlack == False:
    moveForward(c=0.25)
    sleep(0.25)
    onBlack = continuousBlack()

blackTiles = 1
move = [10,10]
c2 = 0.1

while True:
    if blackTiles == 6:
        break
    pivotValue = checkLong()
    move = correctLong(pivotValue, b = 0.25)
    while cs.value() <= blackValue:
        moveForward(move[0], move[1], c=c2)

    c2 = 1.7
    moveForward(move[0],move[1],c=c2)

    onBlack = continuousBlack()

    while onBlack == False:
        moveForward(move[0], move[1], c=0.25)
        sleep(0.25)
        onBlack = continuousBlack()

    blackTiles = blackTiles + 1
    sound.beep()
    c2 = 0.1

#Third Phase
moveForward(0.1)
pivotLeft90()

moveForward(c = 5)

#fourth Phase

detected = False
while detected == False:
    turning(a = 1, b = -1, c = 0.2)
    usv = us.value()
    if(usv <= 300):
        detected = True
sound.beep()

