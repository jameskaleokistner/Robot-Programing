#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor , OUTPUT_B , OUTPUT_C , MoveTank , SpeedPercent
from time import sleep
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor


drive = MoveTank(OUTPUT_B , OUTPUT_C)
cs = ColorSensor()
sound = Sound()

def moveForward(a = 10, b = 10, c = 0.20):
    drive.on_for_rotations(SpeedPercent(a), SpeedPercent(b), c)

def turnLeft(a = -10, b = 10):
    drive.on_for_rotations(SpeedPercent(a), SpeedPercent(b), 0.5)
def turnRight(a = 10, b = -10):
    drive.on_for_rotations(SpeedPercent(a), SpeedPercent(b), 0.5)

def pivotRight():
    drive.on_for_rotations(SpeedPercent(5), SpeedPercent(0), 0.075)
def pivotRight90():
    drive.on_for_rotations(SpeedPercent(10), SpeedPercent(0), 0.5)
def pivotRightReverse():
    drive.on_for_rotations(SpeedPercent(-5), SpeedPercent(0), 0.075)
def pivotLeft():
    drive.on_for_rotations(SpeedPercent(0), SpeedPercent(5), 0.075)
def pivotLeftReverse():
    drive.on_for_rotations(SpeedPercent(0), SpeedPercent(-5), 0.075)
def check():
    count = 0
    while (cs.value() <= 40):
        pivotRightReverse()
        count = count + 1
        sleep(0.1)
    for i in range(count):
        pivotRight()
        sleep(0.1)
    rightPiv = count
    count = 0
    while (cs.value() <= 40):
        pivotLeftReverse()
        count = count + 1
        sleep(0.1)
    for i in range(count):
        pivotLeft()
        sleep(0.1)
    leftPiv = count

    correctPiv = rightPiv - leftPiv
    return correctPiv

def correct(pivotValue):
    if (pivotValue > 0):
        move = [10.5, 10]
    elif (pivotValue < 0):
        move = [10, 10.5]
    else:
        move = [10, 10]
    return move

cs.mode='COL-REFLECT'

sound.speak(str(5) + "rotations")

onBlack = True
blackTiles = 1
sound.beep()
move = [10, 10]
while True:
    if (cs.value() <= 40 and onBlack == False):
        if(blackTiles < 3):
            onBlack = True
            blackTiles = blackTiles + 1
            sound.beep()
        else:
            onBlack = True
            moveForward(c = 0.075)
            blackTiles = blackTiles + 1
            sound.beep()
            pivotValue = check()
            print(pivotValue)
            move = correct(pivotValue)
    elif (cs.value() <= 40):
        onBlack = True
    else:
        onBlack = False

    if (blackTiles >= 7):
        break

    moveForward(move[0], move[1])

sleep(2)
sound.beep()
pivotRight90()
blackTiles = 0

count = 0
while blackTiles < 1:
    if (cs.value() <= 40):
        blackTiles = blackTiles + 1
    moveForward()
    count = count + 1


sound.speak(str(count) + "rotations")

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


