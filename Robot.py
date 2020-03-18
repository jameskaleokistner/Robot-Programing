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

def turn(a = 1, b = 1):
    drive.on_for_rotations(SpeedPercent(a), SpeedPercent(b), 0.025)

def pivotRight():
    drive.on_for_rotations(SpeedPercent(5), SpeedPercent(0), 0.025)
def pivotRight90(a = 20, b = 0, c = 1):
    drive.on_for_rotations(SpeedPercent(a), SpeedPercent(b), c)
def pivotLeft90():
    drive.on_for_rotations(SpeedPercent(0), SpeedPercent(15), 1)
def pivotRightReverse():
    drive.on_for_rotations(SpeedPercent(-5), SpeedPercent(0), 0.025)
def pivotLeft():
    drive.on_for_rotations(SpeedPercent(0), SpeedPercent(5), 0.025)
def pivotLeftReverse():
    drive.on_for_rotations(SpeedPercent(0), SpeedPercent(-5), 0.025)
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
        move = [10, 10.75]
    elif (pivotValue < 0):
        move = [10.75, 10]
    else:
        move = [10, 10]
    return move

def correctLong(pivotValue2):
    if (pivotValue2 > 0):
        move2 = [10, 10.25]
    elif (pivotValue2 < 0):
        move2 = [10.25, 10]
    else:
        move2 = [10, 10]
    return move2

def continuousBlack():
    if cs.value() <= 40:
        moveForward(c=0.1)
        if cs.value() <= 40:
            moveForward(c=-0.05)
            return True
        return False
    else:
        return False


cs.mode='COL-REFLECT'


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
    if (cs.value() <= 40 and onBlack == False):
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
    elif (cs.value() <= 40):
        onBlack = True
    else:
        onBlack = False

    if (blackTiles >= 7):
        break

    moveForward(move[0], move[1])

sleep(2)
sound.beep()
pivotRight90(c = 0.95)


while cs.value() > 40:
    moveForward(c = -0.1)
    sleep(0.25)


moveForward(c = 1.7)
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
    pivotValue = check()
    move = correctLong(pivotValue)
    while cs.value() <= 40:
        moveForward(move[0],move[1],c=c2)

    c2 = 1.7
    moveForward(move[0],move[1],c=c2)

    onBlack = continuousBlack()

    while onBlack == False:
        moveForward(move[0],move[1],c=0.25)
        sleep(0.25)
        onBlack = continuousBlack()

    blackTiles = blackTiles + 1
    sound.beep()
    c2 = 0.1


