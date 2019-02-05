# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Griffin Leonard
# Collaborators (discussion): n/a
# Time: 6:00

import math
import random
import matplotlib
#matplotlib.use("TkAgg")

from ps3_visualize import *
import pylab

# === Provided class Position, do NOT change
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.w = width
        self.h = height
        
        #maps each tile to a dirt amount 
        self.dirt = {} 
        for n in range(self.w):
            for k in range(self.h):
                self.dirt[(n,k)] = dirt_amount
        
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        m,n = math.floor(pos.get_x()),math.floor(pos.get_y())
        
        #sets tile to completely clean if it has less dirt than the robot's capacity
        if self.dirt[(m,n)] - capacity <= 0:
            self.dirt[(m,n)] = 0
        
        #decrease ammount of dirt on a tile by the robot's capacity
        else:
            self.dirt[(m,n)] -= capacity

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        if self.dirt[(m,n)] == 0:
            return True
        return False

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        clean = 0
        for i in self.dirt.values():
            if i == 0:
                clean += 1
        return clean

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        #makes sure position x and y is greater than 0 and within the height and width of the room
        if  pos.get_x() >= 0 and pos.get_x() < self.w and pos.get_y() >= 0 and pos.get_y() < self.h:
            return True
        return False 
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.dirt[(m,n)]
 
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.w * self.h
 
    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        x,y = random.random()*self.w,random.random()*self.h
        return Position(x,y)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        self.position = room.get_random_position() #randomly sets robot's initial position
        self.direction = random.random()*360 #randomly sets robot's initial direction
        self.room = room
        self.speed = speed
        self.cap = capacity

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.position

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class SimpleRobot(Robot):
    """
    A SimpleRobot is a Robot with the standard movement strategy.

    At each time-step, a SimpleRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        #calculates robot's new position
        pos = self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
        
        #if the new position is in the room, move the robot there and clean the tile
        if self.room.is_position_in_room(pos):
            self.set_robot_position(pos)
            self.room.clean_tile_at_position(pos,self.cap)
        #if the new position isn't in the room, change the robot's direction
        else:
            self.set_robot_direction(random.random()*360)

# Uncomment this line to see your implementation of SimpleRobot in action!
#test_robot_movement(SimpleRobot, RectangularRoom)

# === Problem 3
class RobotPlusCat(Robot):
    """
    A RobotPlusCat is a robot with a cat mounted on it. A RobotPlusCat will 
    not clean the tile it moves to and pick a new, random direction for itself 
    with probability p = 0.15 rather than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_cat_probability(prob):
        """
        Sets the probability of the cat messing with the controls equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        RobotPlusCat.p = prob
    
    def gets_cat_interference(self):
        """
        Answers the question: Does the cat mess with this RobotPlusCat's controls
        at this timestep?
        The cat messes with the RobotPlusCat's controls with probability p.

        returns: True if the cat messes with RobotPlusCat's controls, False otherwise.
        """
        return random.random() < RobotPlusCat.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.
        
        Check if the cat messes with the controls. If the robot does get cat
        interference, do not clean the current tile and change its direction randomly.

        If the cat does not mess with the controls, the robot should behave like
        SimpleRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        pos = self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
        
        #if the new position is in the room, move the robot there
        if self.room.is_position_in_room(pos):
            self.set_robot_position(pos)
            #if the cat interferes, also change direction
            if self.gets_cat_interference():
                self.set_robot_direction(random.random()*360)
            #if the cat doesn't interfere, also clean the tile
            else:
                self.room.clean_tile_at_position(pos,self.cap)
        #if the new position isn't in the room, change the robot's direction
        else:
            self.set_robot_direction(random.random()*360)

        
#test_robot_movement(RobotPlusCat, RectangularRoom)


# === Problem 4
class BoostedRobot(Robot):
    """
    A BoostedRobot is a robot that moves extra fast and cleans two tiles in one timestep.

    It moves in its current direction, cleans the tile it lands on, and continues 
    moving in that direction and cleans the second tile it lands on, all in one unit of time. 

    If the BoostedRobot hits a wall when it attempts to move in its current direction,
    it may dirty the current tile by one unit because it moves very fast and can knock dust off of the wall.
    
    There are two possible cases:

    1. The robot starts the timestep on a tile adjacent to the wall, facing it. 
       When it tries moving, it rotates to a random direction, like SimpleRobot.
       It does not dirty the tile with a probability, because it is not traveling fast when it 
       hits the wall. 

    2. The robot starts one tile away from the wall. It moves towards the wall, cleaning the tile
       it moves to and then cannot move further because it hits the wall when it tries moving in that same 
       direction again. After having cleaned the tile, it dirties the current tile by one dirt unit with 
       probability 0.1337 and then rotates in a random direction and stops.
    """
    p = 0.1337

    @staticmethod
    def set_dirty_probability(prob):
        """
        Sets the probability of getting the tile dirty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        BoostedRobot.p = prob
    
    def dirties_tile(self):
        """
        Answers the question: Does this BoostedRobot dirty the tile if it hits the wall at full speed?
        A BoostedRobot dirties a tile with probability p.

        returns: True if the BoostedRobot dirties the tile, False otherwise.
        """
        return random.random() < BoostedRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot is going to hit a wall when it tries moving to the second tile. 
        If it is, clean the tile adjacent to the wall and then dirty it by 1 unit with probability p, 
        and rotate to a random direction.

        If the robot is not going to run into a wall when going to the second tile, the robot should 
        behave like SimpleRobot, but move two tiles at a time (checking if it can move to both new 
        positions and move there if it can, or pick a new direction and stay stationary if it is adjacent 
        to a wall)
        """
        hasSpeed = False #when true, the robot may knock dust off the wall 
        #makes sure the robot moves twice for each timestep
        for i in range(2):
            #calculates robot's new position
            pos = self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
            
            #if the new position is in the room, move the robot there and clean the tile
            if self.room.is_position_in_room(pos):
                self.set_robot_position(pos)
                self.room.clean_tile_at_position(pos,self.cap)
                hasSpeed = True
            else:
                #if the new position isn't in the room and it's the robot's second move 
                #(so it can only do this once per time-step), change the robot's direction
                if i == 1:
                    self.set_robot_direction(random.random()*360)
                
                #if the robot is moving with speed it woun't hit dust off the wall
                if hasSpeed and self.dirties_tile():
                    self.room.clean_tile_at_position(self.get_robot_position(),-1)
                        

#test_robot_movement(BoostedRobot, RectangularRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. SimpleRobot or
                RobotPlusCat)
    """
    totalTime = 0
    for trial in range(num_trials):
        #create the room
        room = RectangularRoom(width, height, dirt_amount)
    
        #create the bots
        bots = []
        for bot in range(num_robots):
            bots.append(robot_type(room, speed, capacity))   
        anim = RobotVisualization(num_robots, width, height, 0.5) #for visual
            
        #run simulation
        timesteps = 0
        while room.get_num_cleaned_tiles()/room.get_num_tiles() < min_coverage:
            for bot in bots:
                bot.update_position_and_clean()
            timesteps += 1
            anim.update(room, bots) # for visual
        
        totalTime += timesteps #update total time-steps of the trials
    return totalTime/num_trials

#print ('SimpleRobot 20x20: ' + str(run_simulation(1, 1.0, 1, 20, 20, 1, 0.80, 1000, SimpleRobot)))
#print ('RobotPlusCat 20x20: ' + str(run_simulation(1, 1.0, 1, 20, 20, 1, 0.80, 1000, RobotPlusCat)))
print ('BoostedRobot 20x20: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.80, 1000, BoostedRobot)),'\n')
#
#print ('10x30 room:\nSimpleRobot: ' + str(run_simulation(2, 1.0, 1, 10, 30, 1, 0.80, 5000, SimpleRobot)))
#print ('RobotPlusCat: ' + str(run_simulation(2, 1.0, 1, 10, 30, 1, 0.80, 5000, RobotPlusCat)))
#print ('BoostedRobot: ' + str(run_simulation(2, 1.0, 1, 10, 30, 1, 0.80, 5000, BoostedRobot)),'\n')
#
#print ('20x15 room:\nSimpleRobot: ' + str(run_simulation(2, 1.0, 1, 10, 30, 1, 0.80, 5000, SimpleRobot)))
#print ('RobotPlusCat: ' + str(run_simulation(2, 1.0, 1, 10, 30, 1, 0.80, 5000, RobotPlusCat)))
#print ('BoostedRobot: ' + str(run_simulation(2, 1.0, 1, 10, 30, 1, 0.80, 5000, BoostedRobot)),'\n')
#
#print ('25x12 room\nSimpleRobot: ' + str(run_simulation(2, 1.0, 1, 25, 12, 1, 0.80, 5000, SimpleRobot)))
#print ('RobotPlusCat: ' + str(run_simulation(2, 1.0, 1, 25, 12, 1, 0.80, 5000, RobotPlusCat)))
#print ('BoostedRobot: ' + str(run_simulation(2, 1.0, 1, 25, 12, 1, 0.80, 5000, BoostedRobot)),'\n')
#
#print ('50x6 room\nSimpleRobot: ' + str(run_simulation(2, 1.0, 1, 50, 6, 1, 0.80, 5000, SimpleRobot)))
#print ('RobotPlusCat: ' + str(run_simulation(2, 1.0, 1, 50, 6, 1, 0.80, 5000, RobotPlusCat)))
#print ('BoostedRobot: ' + str(run_simulation(2, 1.0, 1, 50, 6, 1, 0.80, 5000, BoostedRobot)))


# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room?
#   With num_robots, speed, capacity, and dirt_amount = 1 and num_trials = 1000:
#   BoostedRobot was the best (avg time-step: 438)
#   SimpleRobot was the second best (avg time-step: 795)
#   RobotPlusCat was the worst (avg time-steps: 995)
#   According to the plot, BoostedRobot is much better initially, but as more robots are added,
#   the times decrease exponentially and the time differences quickly decrease 
#
# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#   With speed, capacity, and dirt_amount = 1 and num_trials = 5000:
#   The robots performed about the same in the 10x30 and 20x15 rooms (avg time-steps: Simple 310, PlusCat 404, Boosted 173)
#   In the 25x12 room they were slightly better, especially RobotPlusCat (avg time-steps: Simple 305, PlusCat 387, Boosted 170)
#   They performed the worst in the 50x6 room, especially RobotPlusCat (avg time-steps: Simple 331, PlusCat 514, Boosted 188)
#   The plot once again shows that BoostedRobot is the clear winner

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, SimpleRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, RobotPlusCat))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, BoostedRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('SimpleRobot', 'RobotPlusCat', 'BoostedRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, SimpleRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, RobotPlusCat))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, BoostedRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('SimpleRobot', 'RobotPlusCat', 'BoostedRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
