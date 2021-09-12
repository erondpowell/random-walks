# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
#from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6

from ps2_verify_movement38 import testRobotMovement

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1 === #
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tile_status = {}
        # +1 on range so tiles get named 1 thru len(range(x)), etc.
        for x in range(self.width):
            for y in range(self.height):
                #Is the tile clean? True if clean. False if dirty.
                self.tile_status[(x,y)] = False        
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        #round with ceiling to and account for positions 0.0 to 1.0
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        self.tile_status[(x,y)] = True

    def getTileStatus(self):
        return self.tile_status

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tile_status[(m, n)]

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return(len(self.tile_status))

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        counter = 0
        for v in self.tile_status.values():
            if v == True:
                counter += 1 
        return counter

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = abs(random.randrange(self.width) - random.random())
        y = abs(random.randrange(self.height) - random.random())
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (0 <= pos.getX() < self.width) and (0 <= pos.getY() < self.height)


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        
        self.direction = random.random() * 360     
        self.position = room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)
        
    def getRobotRoom(self):
        """
        Return room that robot is in.
        
        returns: a Room object bound to the robot

        """
        return self.room
       
    def getRobotSpeed(self):
        """
        Return robot speed.
        """
        return self.speed
        
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
    
    def setRobotSpeed(self, new_speed):
        """
        Assumes new_speed is a nonnegative number.
        Updates robot speed.
        """
        self.speed = new_speed
        return self.speed

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction
        

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError
       

# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #Check if next position is still in room.
        next_position = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.getRobotSpeed())
        
        # True if robot's next_position is in Room.
        if self.getRobotRoom().isPositionInRoom(next_position):      
            self.setRobotPosition(next_position)  
            self.getRobotRoom().cleanTileAtPosition(next_position)
        # If False, use the time to get a random direction.
        else:    
            self.setRobotDirection(random.random() * 360)

# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)

# r = RectangularRoom(3,5)              
# x = StandardRobot(r, 1.0)
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


# === Problem 4


def robotGenerator(num_robots, robot_type, robot_room, speed):
    """
    generates num_robots number of robots in a RectangularRoom. 
    Since only generating one type of room, this func also generates room.

    Parameters
    ----------
    num_robots : an integer
        DESCRIPTION: the number of robots in the room
    robot_type : some robot class
        DESCRIPTION: N/A
    robot_room : class RectangularRoom
        DESCRIPTION: The room the robots are in.
    speed : a float
        DESCRIPTION: speed robots move in each time step.

    Returns: a list of robot objects
    """
    robot_army = []    
    for i in range(num_robots):
        robot_army.append(robot_type(robot_room, speed))
    #print('robotGeneratedArmy:', robot_army)
    return robot_army


def singleCleaningSimulation(num_robots, speed, width, height, min_coverage, 
                             robot_type, room_type = RectangularRoom):
    """
    Simulates robot_army cleaning a room.
    Generates a RectangularRoom and robot_army. Cleans room until min_coverage
    is clean. Returns number of time-steps needed to clean.
    -------
    returns: an integer.
    """
    #anim = ps2_visualize.RobotVisualization(num_robots, width, height, 0.01)
    count_time_steps = 0
    robot_room = room_type(width, height)
    robot_army = robotGenerator(num_robots, robot_type, robot_room, speed)
           
    while True:
        #anim.update(robot_room, robot_army)
        count_time_steps += 1     
        for robot in robot_army:
            robot.updatePositionAndClean()  
        #print('printing clean ratio:', robot_room.getNumCleanedTiles() / robot_room.getNumTiles())
        if min_coverage < (robot_room.getNumCleanedTiles() / robot_room.getNumTiles()):
            #anim.done()
            break     
    return count_time_steps


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    all_trials = []
    
    trial = singleCleaningSimulation(num_robots, speed, width, height, min_coverage, robot_type, room_type = RectangularRoom)    
    for i in range(num_trials):
        all_trials.append(trial)
    #print('printing all trials:', all_trials)
    avg_time_step = sum(all_trials) / len(all_trials)

    return avg_time_step


# Uncomment this line to see how much your simulation takes on average
# print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotDirection(random.random() * 360)
        next_position = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.getRobotSpeed())
        
        # True if robot's next_position is in Room.
        if self.getRobotRoom().isPositionInRoom(next_position):      
            self.setRobotPosition(next_position)  
            self.getRobotRoom().cleanTileAtPosition(next_position)
        # # If False, use the time to get a random direction.
        # else:    
        #     self.setRobotDirection(random.random() * 360)

#print(runSimulation(1, 1.0, 10, 10, 0.75, 30, RandomWalkRobot))




def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
    

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
print(showPlot1('robot count effect on clean speed', 'number of robots', 'Time to Clean'))

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
print(showPlot2('floor plan effect on clean speeds', 'floor plan', 'time'))
#
