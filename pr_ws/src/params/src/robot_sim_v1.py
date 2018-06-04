#!/usr/bin/env python
import random

#map states


#robot states

random.seed()
from numpy import complex
from numpy import pi
import numpy
from time import sleep
class Robot():
    EMPTY = 0
    FULL = 1
    WAITING = 2

    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.state = Robot.EMPTY

    def find_move(self, coords, forbidden):
        move_x = self.x
        move_y = self.y

        x_dir = coords[0] - self.x
        y_dir = coords[1] - self.y

        angle = numpy.angle(complex(x_dir,y_dir))

        if (abs(x_dir) < 2 and abs(y_dir) < 2):

            self.state = Robot.FULL if self.state == Robot.EMPTY else Robot.EMPTY
            return self.state == Robot.EMPTY, [self.x , self.y]

        if angle > -pi/8:
            if angle <= pi/8 and not forbidden[0]:
                move_x  = self.x +1
                move_y = self.y 
            elif angle < 3*pi/8 and not forbidden[1]:
                move_x  = self.x +1
                move_y = self.y +1
            elif angle < 5*pi/8 and not forbidden[2]:
                move_x  = self.x 
                move_y = self.y +1            
            elif angle < 7*pi/8 and not forbidden[3]:
                move_x  = self.x -1 
                move_y = self.y +1 
            elif not forbidden[4]:
                move_x  = self.x -1 
                move_y = self.y 
        else:
            if angle > -3*pi/8 and not forbidden[5]:
                move_x  = self.x +1 
                move_y = self.y -1         
            elif angle < -5*pi/8 and not forbidden[6]:
                move_x  = self.x 
                move_y = self.y  -1     
            elif angle < -7*pi/8 and not forbidden[7]:
                move_x  = self.x -1
                move_y = self.y  -1
            elif not forbidden[4]:
                move_x  = self.x -1 
                move_y = self.y 
        return False, [move_x, move_y]


class Board():
    EMPTY = 0
    ROBOT = 1
    CONSTRUCTION = 2
    WAREHOUSE = 5
    def __init__(self, size, robots_number, warehouse_coords, construction_coords):
        self.x = size[0]
        self.y = size[1]
        
        self.base_x = warehouse_coords[0]
        self.base_y = warehouse_coords[1]

        self.building_x = construction_coords[0]
        self.building_y = construction_coords[1]

        self.board = []
        self.robots = []

        self.step_number = 0
        self.packages_delivered = 0

        for i in xrange(0, self.x):
            self.board.append([])
            for j in xrange(0, self.y):
                self.board[i].append(Board.EMPTY)
        
        self.board[self.base_x][self.base_y] = Board.CONSTRUCTION
        self.board[self.building_x][self.building_y] = Board.WAREHOUSE

        

        for x in xrange(0,robots_number):
            x_r = random.randint(0,self.x - 1)
            y_r = random.randint(0,self.y - 1)
            print x_r, y_r
            while self.board[x_r][y_r] != Board.EMPTY:
                x_r = random.randint(0,self.x - 1)
                y_r = random.randint(0,self.y - 1)
            
            self.robots.append(Robot(x_r,y_r))
            self.board[x_r][y_r] = self.ROBOT

    def show(self):
        for j in self.board:
            row = ""
            for k in j:

                if k == self.EMPTY:
                    row = row + " ."
                elif k == self.ROBOT:
                    row = row + " o"
                elif k == self.CONSTRUCTION:
                    row = row + " B"
                elif k == self.WAREHOUSE:
                    row = row + " M"
            print row
        print ("---- STEP: " + str(self.step_number) + " PACKAGES: " + str(self.packages_delivered) + " ----" )
    
    def remove_robots(self):
        for i in xrange(0, self.x):
            for j in xrange(0, self.y):
                if self.board[i][j] == self.ROBOT:
                    self.board[i][j] = self.EMPTY

    def get_forbidden_area(self, coords):
        x = coords[0]
        y = coords[1]

        area = [ [x+1,y], [x+1, y+1], [x, y+1], [x-1, y-1], [x-1, y], [x+1, y-1], [x, y-1], [x-1, y-1] ]
        forbidden  = []
        for a in area:
            if a[0] >= 0 and a[1] >=0 and a[0] < self.x and a[1] < self.y:
                forbidden.append(self.board[a[0]][a[1]] != self.EMPTY)
            else:
                forbidden.append(True)
        return forbidden

    def step(self):
        list_of_moves  = []
        for robot in self.robots:
            if robot.state == robot.EMPTY:
                new_pack, this_move = robot.find_move([self.base_x, self.base_y], self.get_forbidden_area([robot.x, robot.y]))
            elif robot.state == robot.FULL:
                new_pack, this_move = robot.find_move([self.building_x, self.building_y], self.get_forbidden_area([robot.x, robot.y]))
                
            if new_pack:
                self.packages_delivered +=1
            able_to_move = True
            for move in list_of_moves:
                if this_move == move:
                    able_to_move = False
            if able_to_move:
                list_of_moves.append(this_move)
                robot.x = list_of_moves[-1][0]
                robot.y = list_of_moves[-1][1]
            else:
                list_of_moves.append([robot.x, robot.y])


        self.remove_robots()
        for move in list_of_moves:
            self.board[move[0]][move[1]] = self.ROBOT
        self.step_number +=1

sim = Board([30,20],5,[0,15],[25,8])
for x in xrange(0,200):
    sim.show()
    sim.step()
    sleep(0.15)
