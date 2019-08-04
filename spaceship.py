#!/usr/bin/env python

import Tkinter as tk
import math
import copy
from messages import *

WATER_COLOR = "blue"
SHIP_COLOR = "grey"
HIT_COLOR = "red"
OFFEST_COLOR = "white"
CELL_SIZE = 30
CELLS_PER_ROW = 10
WINDOW_WIDTH = CELL_SIZE * CELLS_PER_ROW
OFFSET = CELL_SIZE * 2
WINDOW_HEIGHT = (WINDOW_WIDTH * 2) + OFFSET
MAP_HEIGHT = WINDOW_WIDTH
BOT_MAP_TOP = WINDOW_WIDTH + OFFSET
SHIP_TO_BE_PLACED = 4
READY = False
RECV = receiver("0.0.0.0", 4556)
SEND = sender("10.0.0.215", 4556)

my_cells = list()
e_cells = list()
root = tk.Tk()
c = tk.Canvas(root, width = WINDOW_WIDTH, 
height = WINDOW_HEIGHT, background = WATER_COLOR)
c.pack()

run = tk.Tk()
b = tk.Button(run, height = 2, 
width = 15, text="SUBMIT", command = lambda: After_Startup())
b.grid(row=0, column=0)
b.pack()

###############################################################################
# ALL CLASSES LIVE HERE
###############################################################################
class Cell():
    def __init__(self, x, y):
        self.isShip = False
        self.hit = False
        self.x = x
        self.y = y

###############################################################################
# ALL MESSAGE FUNCTIONS LIVE HERE
###############################################################################
def After_Startup():
    global READY
    SEND.sendMessage(-1, -1, -1)
    if SHIP_TO_BE_PLACED > 0:
        return False
    else:
        READY = True
        c.create_rectangle(0, WINDOW_WIDTH,
     WINDOW_WIDTH, WINDOW_WIDTH + OFFSET, fill = OFFEST_COLOR)
        c.after(1000, Recv)
        return True

def Recv():
    RECV.receivePoll()
    c.after(1000, Recv)

###############################################################################
# ALL MATH FUNCTIONS LIVE HERE
###############################################################################
def Convert_To_Small(x, y):
    px = x / CELL_SIZE
    py = -1
    if y >= BOT_MAP_TOP:
        py = (y - BOT_MAP_TOP) / CELL_SIZE
    elif y < MAP_HEIGHT:
        py = y / CELL_SIZE
    return (px, py)

def Check_Hit(x, y):
    for i in e_cells:
        for cell in i:
            if cell.x == x and cell.y == y:
                return True
    return False

def Is_Dead_Ship(x, y):
    for i in e_cells:
        for cell in i:
            if (cell.x == x and cell.y == y) and \
            (cell.hit != True and cell.isShip == True):
                return False
    return True

def Check_Win(x, y):
    for i in e_cells:
        for j in i:
            if not (Is_Dead_Ship(x, y)):
                return False
    return True

def Roundup(x):
    return int(math.ceil(x / CELL_SIZE)) * CELL_SIZE

def Find_Click(event):
    return (Roundup(event.x), Roundup(event.y))

def Find_My_Cell(point):
    for i in my_cells:
        for cell in i:
            (x,y) = Convert_To_Small(point[0], point[1])
            if x == cell.x and y == cell.y:
                return cell
    return None

def In_My_Board(point):
    if point[1] < BOT_MAP_TOP:
        return False
    return True

def In_E_Board(point):
    if point[1] < MAP_HEIGHT:
        return True
    return False

def In_Offset(point):
    if point[1] < BOT_MAP_TOP and point[1] > WINDOW_WIDTH:
        return True
    return False

def Can_Be_Placed(cells):
    for cell in cells:
        if cell.y > WINDOW_HEIGHT or cell.y < BOT_MAP_TOP:
            return False
    return True

def Draw_Ships_Left():
    global SHIP_TO_BE_PLACED
    c.create_rectangle(0, WINDOW_WIDTH,
     WINDOW_WIDTH, WINDOW_WIDTH + OFFSET, fill = OFFEST_COLOR)
    c.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial",
     text="YOU NEED TO PLACE {} MORE SHIPS".format(SHIP_TO_BE_PLACED))

def Update_Cell(point):
    global SHIP_TO_BE_PLACED
    global READY
    if In_My_Board(point) and SHIP_TO_BE_PLACED >= 0:
        cell = Find_My_Cell(point)
        if not cell.isShip and SHIP_TO_BE_PLACED > 0:
            cell.isShip = True
            SHIP_TO_BE_PLACED = SHIP_TO_BE_PLACED - 1
            c.create_rectangle(point[0], point[1], 
                point[0] + CELL_SIZE, point[1] + CELL_SIZE, fill = SHIP_COLOR) 
        else:
            cell.isShip = False
            SHIP_TO_BE_PLACED = SHIP_TO_BE_PLACED + 1
            c.create_rectangle(point[0], point[1], 
                point[0] + CELL_SIZE, point[1] + CELL_SIZE, fill = WATER_COLOR) 
    elif In_E_Board(point) and SHIP_TO_BE_PLACED == 0 and READY:
        cell = Find_My_Cell(point)
        cell.hit = True
        # SEND FIRE MESSAGE

###############################################################################
# ALL DRAW FUNCTIONS LIVE HERE
###############################################################################
def Draw_Click(point):
    global SHIP_TO_BE_PLACED
    global READY
    if In_E_Board(point) and SHIP_TO_BE_PLACED == 0 and READY:
        c.create_rectangle(point[0], point[1], 
            point[0] + CELL_SIZE, point[1] + CELL_SIZE, fill = HIT_COLOR)

def Draw_Lines():
    for i in range(CELLS_PER_ROW + 1):
        c.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, WINDOW_WIDTH)
        c.create_line(0, i * CELL_SIZE, WINDOW_WIDTH, i * CELL_SIZE)
        c.create_line(i * CELL_SIZE, 
        BOT_MAP_TOP, i * CELL_SIZE, WINDOW_HEIGHT)
        c.create_line(0, (i * CELL_SIZE) + BOT_MAP_TOP, 
        WINDOW_WIDTH, (i * CELL_SIZE) + BOT_MAP_TOP)

###############################################################################
# HANDLE CLICK
###############################################################################
def Callback(event):
    point = Find_Click(event)
    Draw_Click(point)
    Update_Cell(point)
    Draw_Ships_Left()

def Print_Cells():
    for i in my_cells:
        for cell in i:
            print("X {} Y {}".format(cell.x, cell.y))

###############################################################################
# INIT
###############################################################################
def Init_Cells():
    for i in range(0, CELLS_PER_ROW):
        my_row = list()
        e_row = list()
        for j in range(0, CELLS_PER_ROW):
            my_row.append(Cell(i, j))
            e_row.append(Cell(i, j))
        my_cells.append(my_row)
        e_cells.append(e_row)

###############################################################################
# MAIN
###############################################################################
if __name__=="__main__":
    Init_Cells()
    Draw_Lines()
    Draw_Ships_Left()
    c.bind('<Button-1>', Callback)
    
    tk.mainloop()