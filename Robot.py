#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor , OUTPUT_B , OUTPUT_C , MoveTank , SpeedPercent
from time import sleep
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor


drive = MoveTank(OUTPUT_B , OUTPUT_C)
cs = ColorSensor()
sound = Sound()

def moveForward():
    drive.on_for_rotations(SpeedPercent(10), SpeedPercent(10), 0.25)

def turnLeft():
    drive.on_for_rotations(SpeedPercent(-10), SpeedPercent(10), 0.5)
def turnRight():
    drive.on_for_rotations(SpeedPercent(10), SpeedPercent(-10), 0.5)
def pivotRight():
    drive.on_for_rotations(SpeedPercent(10), SpeedPercent(0), 0.1)
def pivotLeft():
    drive.on_for_rotations(SpeedPercent(10), SpeedPercent(0), 0.1)
def correct():
    count = 0
    while (cs.value() <= 40):
        pivotRight()
        count = count + 1
    for i in len(count):
        pivotRightReverse()
    rightPiv = count
    count = 0
    while (cs.value() <= 40):
        pivotLeft()
        count = count + 1
    for i in len(count):
        pivotLeftReverse()
    leftPiv = count

    correctPiv = rightPiv - leftPiv

    if (correctPiv < 0):
        correctLeft()
    elif(correctPiv > 0):
        correctRight()

cs.mode='COL-REFLECT'

onBlack = False
blackTiles = 0
while True:
    if (cs.value() <= 40 and onBlack == False):
        onBlack = True
        blackTiles = blackTiles + 1
        sound.beep()
        correct()
    elif (cs.value() <= 40):
        onBlack = True
    else:
        onBlack = False

    if (blackTiles >= 7):
        break

    moveForward()
sleep(2)
turn90Right()
sleep(2)
moveForward()
moveForward()
moveForward()
blackTiles = 0
#continuous = True
'''while True:
    if (cs.value() <= 40 and continuous):
        blackTiles = blackTiles + 1 '''






'''while True:
    while (cs.value() <= 25):
        moveForward()
    while (cs.value() >= 25 and rt == True):
        turnRight()
    while (cs.value() >= 25 and rt == False):
        turn90Left()

    if(rt == True):
        turnleft()
        rt = False
    else:
        turnRight()
        rt = True'''



