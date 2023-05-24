import copy
from timeit import default_timer as timer
from turtle import *
from random import *

class square:
    def __init__(self, location, size, color, fill=False):
        self.location = location
        self.size = size
        self.color = color
        self.fill = fill
        self.width = size
        self.height = size

    def draw(self, turtle):
        turtle.pu()
        turtle.setpos(self.location)
        turtle.pd()
        turtle.color(self.color)
        if (self.fill):
            turtle.begin_fill()
        for _ in range(4):
            turtle.fd(self.size)
            turtle.lt(90)
        if (self.fill):
            turtle.end_fill()
        turtle.ht()

#    0  1  2  3  4  5  6  7
# 0  *  *  *  *  *  *  *  *
# 1  *  *  *  *  *  *  *  *
# 2  *  *  *  *  *  *  *  *
# 3  *  *  *  *  *  *  *  *
# 4  *  *  *  *  *  *  *  *
# 5  *  *  *  *  *  *  *  *
# 6  *  *  *  *  *  *  *  *
# 7  *  *  *  *  *  *  *  *

EXENV1 = [[0,0,0,0,0,0,0,0],
          [0,0,1,1,1,1,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,1,1,0,0],
          [0,1,1,0,0,0,0,0],
          [0,1,0,0,0,1,1,1],
          [0,1,0,0,0,0,1,0],
          [0,0,0,0,0,0,0,0]]

EXENV2 = [[0,0,0,0,0,0,0,0],
          [0,0,1,1,1,1,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,1,1,0,0],
          [0,1,1,0,0,0,0,0],
          [0,1,0,0,0,1,1,1],
          [0,1,1,0,0,0,1,0],
          [0,0,0,0,0,0,0,0]]

EXENV3 = [[0,0,0,0,0,0,0,0],
          [0,1,1,1,1,1,1,0],
          [0,1,0,0,0,0,0,0],
          [0,1,0,1,1,1,1,1],
          [0,1,0,0,0,0,0,0],
          [0,1,1,1,1,1,1,0],
          [0,0,0,0,0,0,0,0],
          [0,1,1,1,1,1,1,1]]

EXENV4 = [[0,0,0,1,0,0,0,0,0,0],
          [0,0,0,1,1,1,0,0,1,0],
          [1,0,0,0,0,0,0,1,1,1],
          [1,1,0,0,0,1,1,0,0,0],
          [1,1,1,0,0,0,0,0,0,1],
          [0,1,0,0,0,1,1,0,0,1],
          [0,1,1,1,1,0,0,0,1,0],
          [0,1,1,1,1,1,1,0,1,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0]]

HAPPYFACE = [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [1,0,0,0,1],
             [0,1,1,1,0]]

def isLegal(env, y, x):
    # Determines if going to y, x is legal
    # legal = not out of bounds, not into an obstacle
    # RETURNS: Bool

    if y > len(env)-1 or x > len(env[y])-1 or y < 0 or x < 0:
        return False
    if env[y][x] == 1:
        return False
    return True

assert isLegal(EXENV1, 8, 2) == False
assert isLegal(EXENV1, 1, 2) == False
assert isLegal(EXENV1, 1, 1) == True

def isRepeat(path, y, x):
    if (y, x) in path:
        return True
    return False

assert isRepeat([(6, 2), (7, 2), (7, 3)], 7, 3) == True
assert isRepeat([(6, 2), (7, 2), (7, 3)], 7, 4) == False

def legalSteps(env, y, x):
    # Determines 0-4 new possible positions from y, x
    # Checks in the order of up, down, left, right
    # RETURNS: [()] or False if no legal positions found

    steps = []
    for vert in range(-1, 2, 2):
        if isLegal(env, y+vert, x):
            steps.append((y+vert, x))
    for horiz in range(-1, 2, 2):
        if isLegal(env, y, x+horiz):
            steps.append((y, x+horiz))

    return steps

assert legalSteps(EXENV1, 7, 2) == [(6, 2), (7, 1), (7, 3)]
assert legalSteps(EXENV1, 6, 7) == [(7, 7)]

def findBestPath(env, y0, x0, y1, x1):
    # Finds the first path from y0, x0 that leads to y1, x1
    # RETURNS: [(y, x)] List of path steps

    paths = [[(y0, x0)]]
    for p in paths:
        if (y1, x1) in p:
            return p
        print(len(paths))
        for step in legalSteps(env, p[-1][0], p[-1][1]):
            if isRepeat(p, step[0], step[1]):
                continue
            path = copy.deepcopy(p)
            path.append(step)
            paths.append(path)
    return False

def findFastPath(env, y0, x0, y1, x1):
    # Finds the first path from y0, x0 that leads to y1, x1
    # RETURNS: [(y, x)] List of path steps

    paths = [[(y0, x0)]]
    for index, p in enumerate(paths):
        if (y1, x1) in p:
            return p
        print(len(paths))
        for step in legalSteps(env, p[-1][0], p[-1][1]):
            if isRepeat(p, step[0], step[1]):
                continue
            path = copy.deepcopy(p)
            path.append(step)
            paths.insert(index+1, path)
    return False

def displayPathASCII(env, path):
    for p in path:
        env[p[0]][p[1]] = 8
    env[path[0][0]][path[0][1]] = 2
    env[path[-1][0]][path[-1][1]] = 2
    for e in env:
        print(e)

def displayPathTurtle(env, path):
    if path == False:
        return

    t = Turtle()
    t.speed(0)
    t.color('white')
    t.pensize(8)

    # This functions assumes a square env
    # Draws the bounding box
    ySize = len(env)
    xSize = len(env[0])
    t.pu()
    t.setpos(-300, 300)
    t.pd()
    t.goto(300, 300)
    t.goto(300, -300)
    t.goto(-300, -300)
    t.goto(-300, 300)

    # Draws wall obstacles
    # Draws start and end points
    for indy, y in enumerate(reversed(range(-300, 300, int(600/ySize)))):
        for indx, x in enumerate(range(-300, 300, int(600/xSize))):
            if env[indy][indx] == 1:
                square((x, y), 600/ySize, 'white', fill=True).draw(t)
            elif (indy, indx) == path[0]:
                square((x+(600/ySize/4), y+(600/ySize/4)), 600/ySize/2, 'green', fill=True).draw(t)
            elif (indy, indx) == path[-1]:
                square((x+(600/ySize/4), y+(600/ySize/4)), 600/ySize/2, 'red', fill=True).draw(t)

    # Draws path
    unit = 600/ySize
    t.pu()
    t.setpos(-300+(unit*path[0][1])+(unit/2), 300-(unit*path[0][0])-(unit/2))
    t.pd()
    t.speed(2)

    directions = []
    for c in range(1, len(path)):
        if path[c][0] < path[c-1][0]:
            directions.append('u')
        elif path[c][0] > path[c-1][0]:
            directions.append('d')
        elif path[c][1] < path[c-1][1]:
            directions.append('l')
        elif path[c][1] > path[c-1][1]:
            directions.append('r')

    t.color('black')
    for d in directions:
        if d == 'u':
            t.goto(t.pos()[0], t.pos()[1]+unit)
        elif d == 'd':
            t.goto(t.pos()[0], t.pos()[1]-unit)
        elif d == 'r':
            t.goto(t.pos()[0]+unit, t.pos()[1])
        elif d == 'l':
            t.goto(t.pos()[0]-unit, t.pos()[1])

def genRandomBoard(size):
    board = []
    myList = [0] * 5 + [1] * 3
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(choice(myList))
        board.append(row)
    print(len(board))
    return board

def genRandomStarEndPos(board):
    # def start(board):
    #     for y in range(len(board)):
    #         for x in range(len(board)):
    #             if board[y][x] == 0:
    #                 return (y, x)

    # def end(board):
    #     for y in reversed(range(len(board))):
    #         for x in reversed(range(len(board))):
    #             if board[y][x] == 0:
    #                 return(y, x)
    # return start(board), end(board)
    potentials = []
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == 0:
                potentials.append((y, x))
    start = choice(potentials)
    potentials.remove(start)
    end = choice(potentials)
    return start, end

# start = timer()

# for r in findBestPath(EXENV4, 0, 4, 5, 0):
#     print(r)

# end = timer()
# print('\nTime to solve: {} seconds\n'.format(end-start))

# while True:

wn = Screen()
wn.colormode(255)
wn.bgcolor(255, 205, 46)
wn.title('Path Finding')
#wn.tracer(0)
wn.setup(width=1.0, height=1.0)

    # path = False
    # while not path:
    #     board = genRandomBoard(8)
    #     start, end = genRandomStarEndPos(board)
    #     path = findBestPath(board, start[0], start[1], end[0], end[1])
    #     if path == False or len(path) < len(board):
    #         path = False

    # displayPathTurtle(board, path)

displayPathTurtle(EXENV4, findBestPath(EXENV4, 0, 4, 5, 0))

    # wn.clearscreen()
    # wn.update()
done()