# 6.0002 Problem Set 3:
#
# Visualization code for simulated robots.
#
# See the problem set for instructions on how to use this code.

import math
import time
import random
import base64
import matplotlib
from tkinter import *
from urllib.request import urlopen

#matplotlib.use('TkAgg')

class RobotVisualization:
    def __init__(self, num_robots, width, height, delay = 0.2):
        "Initializes a visualization with the specified parameters."
        # Number of seconds to pause after each frame
        self.delay = delay

        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.num_robots = num_robots
        
        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()
        
        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Draw gray squares for dirty tiles
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                if (i, j) not in self.tiles:
                    self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2,
                                                                 fill = "black")
                else:
                    self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, 
                                                                   fill = "red")
                                                                  

        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)

        # Draw some status text
        self.robots = None
        self.text = self.w.create_text(25, 0, anchor=NW,
                                       text=self._status_string(0, 0, 1))
        self.time = 0

        # Bring window to front and focus
        self.master.attributes("-topmost", True)  # Brings simulation window to front upon creation
        self.master.focus_force()                 # Makes simulation window active window
        self.master.attributes("-topmost", False) # Allows you to bring other windows to front
        
        self.master.update()
        
        

    def _status_string(self, time, num_clean_tiles, num_total_tiles):
        "Returns an appropriate status string to print."
        percent_clean = 100 * num_clean_tiles / float(num_total_tiles)
        return "Time: %04d; %d tiles (%d%%) cleaned" % \
            (time, num_clean_tiles, percent_clean)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_robot(self, position, direction):
        "Returns a polygon representing a robot with the specified parameters."
        x, y = position.get_x(), position.get_y()
        d1 = direction + 165
        d2 = direction - 165
        x1, y1 = self._map_coords(x, y)
        x2, y2 = self._map_coords(x + 0.6 * math.sin(math.radians(d1)),
                                  y + 0.6 * math.cos(math.radians(d1)))
        x3, y3 = self._map_coords(x + 0.6 * math.sin(math.radians(d2)),
                                  y + 0.6 * math.cos(math.radians(d2)))
        return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="red")

    def update(self, room, robots):
        "Redraws the visualization with the specified room and robot state."

        # Delete all unfurnished tiles
        for tile in self.tiles:
            self.w.delete(self.tiles[tile])

        # Redraw dirty tiles
        self.tiles = {}
        for i in range(self.width):
            for j in range(self.height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                if not room.is_tile_cleaned(i, j):
                    #get dirt amount
                    dirtAmount = room.get_dirt_amount(i, j)
                    color = 150
                    color = int(color/dirtAmount)
                    r = color
                    g = color
                    b = color
                    rgb = r, g, b
                    Hex = '#%02x%02x%02x' % rgb
                    self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = str(Hex))
                    
        # Delete all existing robots.
        if self.robots:
            for robot in self.robots:
                self.w.delete(robot)
                self.master.update_idletasks()
        # Draw new robots
        self.robots = []
        for robot in robots:
            pos = robot.get_robot_position()
            x, y = pos.get_x(), pos.get_y()
            x1, y1 = self._map_coords(x - 0.08, y - 0.08)
            x2, y2 = self._map_coords(x + 0.08, y + 0.08)
            self.robots.append(self.w.create_oval(x1, y1, x2, y2,
                                                  fill = "black"))
            self.robots.append(
                self._draw_robot(robot.get_robot_position(), robot.get_robot_direction()))
        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(
            25, 0, anchor=NW,            
            text=self._status_string(self.time, room.get_num_cleaned_tiles(), room.get_num_tiles()))
        self.master.update()
        time.sleep(self.delay)

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()

class CatVisualization(RobotVisualization):
    def __init__(self, num_robots, width, height, delay = 0.2):
        super().__init__(num_robots, width, height, delay)
        # pull a random image from the interwebs        
        self.cat_images = [\
        "https://orig00.deviantart.net/aaa1/f/2015/204/c/4/cookie_cat_icon_by_nega_the_impmon9508-d92i10o.gif",
        "https://i.imgur.com/LSq9D7L.gif",
        "https://mlpforums.com/uploads/post_images/img-2896624-1-Nyan_Cat_Emoticon.gif",
        "https://pic.chinesefontdesign.com/uploads/2017/01/chinesefontdesign.com_2017-01-10_18-06-50.gif",
        "http://www.animationplayhouse.com/calico.gif",
        "http://www.clipartbest.com/cliparts/RiG/Bpq/RiGBpqy6T.gif",
        "https://pic.chinesefontdesign.com/uploads/2017/03/chinesefontdesign.com_2017-03-28_09-04-00.gif",
        "http://24.media.tumblr.com/278bc46c09873f19bfa43fd879fd4428/tumblr_mq1198mVly1sabpmro1_500.gif"
        ]
        self.cat_url = random.choice(self.cat_images)
        self.img = None
        
    def _draw_robot(self, position, direction):
        "Returns a cat icon representing a CatOnARobot"
        if self.img is None:
            image_byt = urlopen(self.cat_url).read()
            image_b64 = base64.encodestring(image_byt)
            photo = PhotoImage(data=image_b64)
            self.img = photo.subsample(int(photo.height()/60))
            #self.img = photo
        x, y = position.get_x(), position.get_y()
        x1, y1 = self._map_coords(x, y)
        return self.w.create_image(x1, y1, image=self.img, anchor='center')

    def _draw_direction(self, position, direction):
        "Returns a polygon representing a direction with the specified parameters."
        x, y = position.get_x(), position.get_y()
        d1 = direction + 165
        d2 = direction - 165
        x1, y1 = self._map_coords(x, y)
        x2, y2 = self._map_coords(x + 0.6 * math.sin(math.radians(d1)),
                                  y + 0.6 * math.cos(math.radians(d1)))
        x3, y3 = self._map_coords(x + 0.6 * math.sin(math.radians(d2)),
                                  y + 0.6 * math.cos(math.radians(d2)))
        return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="red")
    
    
    def update(self, room, robots):
        "Redraws the visualization with the specified room and robot state."

        # Delete all unfurnished tiles
        for tile in self.tiles:
            self.w.delete(self.tiles[tile])

        # Redraw dirty tiles
        self.tiles = {}
        for i in range(self.width):
            for j in range(self.height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                if not room.is_tile_cleaned(i, j):
                    #get dirt amount
                    dirtAmount = room.get_dirt_amount(i, j)
                    color = 150
                    color = int(color/dirtAmount)
                    r = color
                    g = color
                    b = color
                    rgb = r, g, b
                    Hex = '#%02x%02x%02x' % rgb
                    self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = str(Hex))
                    
        # Delete all existing robots.
        if self.robots:
            for robot in self.robots:
                self.w.delete(robot)
                self.master.update_idletasks()
        # Draw new robots
        self.robots = []
        for robot in robots:
            pos = robot.get_robot_position()
            x, y = pos.get_x(), pos.get_y()
            x1, y1 = self._map_coords(x - 0.08, y - 0.08)
            x2, y2 = self._map_coords(x + 0.08, y + 0.08)
            #self.robots.append(self.w.create_oval(x1, y1, x2, y2,
            #                                      fill = "black"))
            self.robots.append(
                self._draw_robot(robot.get_robot_position(), robot.get_robot_direction()))
            self.robots.append(
                self._draw_direction(robot.get_robot_position(), robot.get_robot_direction()))

        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(
            25, 0, anchor=NW,            
            text=self._status_string(self.time, room.get_num_cleaned_tiles(), room.get_num_tiles()))
        self.master.update()
        time.sleep(self.delay)
        

def test_robot_movement(robot_type, room_type):
    
    room = room_type(5, 5, 4)
    robots = [robot_type(room, 1, 1)]
    coverage = 0
    time_steps = 0
    min_coverage = 1.0
    # Hacky way to check which visualization we're using without import from ps3
    if "RobotPlusCat" in str(robot_type):
        anim = CatVisualization(1,5,5) 
    else:
        anim = RobotVisualization(1, 5, 5)  
    while coverage < min_coverage:
        time_steps += 1 
        for robot in robots:
            robot.update_position_and_clean()
            anim.update(room, robots)
            coverage = float(room.get_num_cleaned_tiles())/room.get_num_tiles()
    anim.done()
