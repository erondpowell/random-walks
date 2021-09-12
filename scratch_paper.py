#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 13:43:24 2021

@author: EronDonevan
"""
import random
import ps2_working as classes

#Instantiating a RextangularRoom object
room = classes.RectangularRoom(3,5)


# === Test all Methods Below

# test getNumTiles
print(room.getNumTiles())


# ==  test  cleanTileAtPosition  and  getTileStatus
roomba = classes.Position(0.4, 4)
room.cleanTileAtPosition(roomba)

print('checking cleanTilePosition:', room.getTileStatus())


# == test isTileCleaned(m, n)
print('checking if isTileCleaned:', room.isTileCleaned(2,4))


# == test getNumTiles
print('Checking getNumTiles:', room.getNumTiles())


# == test getNumCleanedTiles
print('Checking getNumCleanedTiles:', room.getNumCleanedTiles())

# == test getRandomPosition
print('Checking getRandomPosition:', room.getRandomPosition())

# == test isPositionInRoom
print('Checking isPositionInRoom:', room.isPositionInRoom(classes.Position(0.1,4)))


# == test 
print(random.random() * 360)



# ===== Testing Standard Robot

# r = classes.RectangularRoom(3,5)              
# x = classes.StandardRobot(r, 3.0)

# print(x.updatePositionAndClean())
# print(x.getRobotRoom().getTileStatus())
# print(x.updatePositionAndClean())
# print(x.getRobotRoom().getTileStatus())
# print(x.updatePositionAndClean())
# print(x.getRobotRoom().getTileStatus())
# print(x.updatePositionAndClean())
# print(x.getRobotRoom().getTileStatus())
# print(x.updatePositionAndClean())
# print(x.getRobotRoom().getTileStatus())
# print(x.updatePositionAndClean())
# print(x.getRobotRoom().getTileStatus())
# print(x.updatePositionAndClean())
# print(x.getRobotRoom().getTileStatus())


# ===== Testing roomGenerator()

# print(classes.roomGenerator(3,5).getNumTiles())
# prints as <ps2_working.RectangularRoom object at 0x7f9408aea3a0>


# ===== Testing robotGenerator()


# ===== Testing funcy shit

print(8300/537)

for i in range(20):
    i
    print(i>>1,i//2)


Lo = ['apples', 'oranges', 'kiwis', 'pineapples']

def stdDevOfLengths(L):
    
    if len(L) == 0:
        return float('NaN')
    
    str_to_num = []
    variance = 0
    
    for word in L:
        str_to_num.append(len(word))
        
    print('printing str to num:', str_to_num)
    avg_len = sum(str_to_num)/len(str_to_num)
    
    print('avg len:', avg_len)
    for length in str_to_num:
        variance += ((length - avg_len)**2)
    print('variance:', variance)
    return (variance / len(L))**0.5

print(Lo)


def coefOfLengths(bf):
    variance = 0
    avg_len = sum(bf)/len(bf)

    for i in bf:
        variance += ((i - avg_len)**2)
        
    return ((variance / len(bf))**0.5) / avg_len

print(coefOfLengths([10, 4, 12, 15, 20, 5]))




# ==== Monte Carlo Green/Red Balls


# def noReplacementSimulation(numTrials):
#     '''
#     Runs numTrials trials of a Monte Carlo simulation
#     of drawing 3 balls out of a bucket containing
#     3 red and 3 green balls. Balls are not replaced once
#     drawn. Returns a decimal - the fraction of times 3 
#     balls of the same color were drawn.
#     '''

#     threeOfAKind = 0
    
#     for trial in range(numTrials):
#         # above 0 - 0.5 is red. > 0.5 is green.
#         t1 = random.random()
#         t2 = random.random()
#         t3 = random.random()
        
 
#             threeOfAKind += 1
        
#     return (threeOfAKind / numTrials)
    
    
#     1/2
#     2/5
#     1/4
    
    
def noReplacementSimulation(numTrials): 
    threeOfAKind = 0

    for trial in range(numTrials):
        draw = []
        bucket = ['red', 'red', 'red', 'green', 'green', 'green']

        for ball in range(3):
            draw.append(bucket.pop(random.randrange(0, (len(bucket)))))
            
        if (draw[0] == draw[1]) and (draw[1] == draw[2]):
            threeOfAKind += 1

    return (threeOfAKind / numTrials)



print(noReplacementSimulation(100))

    
    
    
    
   
    
    
