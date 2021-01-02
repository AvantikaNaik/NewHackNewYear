from cmu_112_graphics import *
import random

# Snake is the player
# Worm is the AI

class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.distance = 0
        self.heuristic = 0
        self.cost = 0

    def __eq__(self, other):
        return (isinstance(other, Node) and self.position == other.position)

    def __repr__(self):
        return f"Node at {self.position} with f={self.cost}"

    def __hash__(self):
        return hash((self.parent, self.position, self.distance, self.heuristic, self.cost))

def appStarted(app):
    app.rows = 20
    app.cols = 20
    app.margin = 5 # margin around grid
    app.timerDelay = 250
    initSnakeAndWormAndFood(app)
    app.waitingForFirstKeyPress = True

def initSnakeAndWormAndFood(app):
    app.snake = [(0,0)]
    app.direction = (0, +1) # (drow, dcol)
    app.gameOver = False
    app.worm = [(app.rows-1, app.cols-1)]
    app.wormdirection = (-1,0) #(drow, dcol)
    placeFood(app)

def astar(app, startval, endval):
    # Init start and end nodes, and lists
    start = Node(None, startval)
    end = Node(None, endval)
    openList = []
    closedList = set()
    openList.append(start)

    # Loop until you find end
    while len(openList) > 0:
        current = openList[0]
        bestNode = 0
        for i in range(len(openList)):
            if current.cost > openList[i].cost:
                current = openList[i]
                bestNode = i

        openList.pop(bestNode)
        closedList.add(current)
        # if you're at end, return path (backtrackingly)
        if current == end:
            path = []
            tempcurrent = current
            while tempcurrent != None:
                path.append(tempcurrent.position)
                tempcurrent = tempcurrent.parent
            return path[::-1]

        children = []
        # children are adjacent nodes
        for (drow, dcol) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            row = current.position[0] + drow
            col = current.position[1] + dcol
            if 0 <= row < app.rows and 0 <= col < app.cols and wormCanMove(app, drow, dcol, row, col) : 
                new_node = Node(current, (row,col))
                children.append(new_node)

        # Thanks to TA Elena H for helping me debug this part! 
        for child in children:
            if child not in closedList:
                child.distance = current.distance + 1
                child.heuristic = ((child.position[0] - end.position[0]) ** 2) + ((child.position[1] - end.position[1]) ** 2)
                child.cost = child.distance + child.heuristic  
            if child not in openList:                    
                openList.append(child)

def wormCanMove(app, drow, dcol, row, col):
    if (row + drow , col + dcol) in app.snake:
        return False
    return True

def moveWorm(app):
    wormRow, wormCol = app.worm[0]
    foodRow, foodCol = app.foodPosition
    start = (wormRow, wormCol)
    end = (foodRow, foodCol)
    path = astar(app, start, end)
    nextRow, nextCol = path[1]
    if nextRow > wormRow:
        if nextCol > wormCol:
            app.wormdirection = (+1, +1)
        elif nextCol < wormCol:
            app.wormdirection = (+1, -1)
        else:
            app.wormdirection = (+1, 0)
    elif nextRow < wormRow:
        if nextCol > wormCol:
            app.wormdirection = (-1, +1)
        elif nextCol < wormCol:
            app.wormdirection = (-1, -1)
        else:    
            app.wormdirection = (-1, 0)
    else:
        if nextCol > wormCol:
            app.wormdirection = (0, +1)
        elif nextCol < wormCol:
            app.wormdirection = (0, -1)
        else:
            app.wormdirection = (0, 0)


# getCellBounds from grid-demo.py
def getCellBounds(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def keyPressed(app, event):
    if (app.waitingForFirstKeyPress):
        app.waitingForFirstKeyPress = False
    elif (event.key == 'r'):
        initSnakeAndWormAndFood(app)
    elif app.gameOver:
        return
    elif (event.key == 'Up'):      app.direction = (-1, 0)
    elif (event.key == 'Down'):  app.direction = (+1, 0)
    elif (event.key == 'Left'):  app.direction = (0, -1)
    elif (event.key == 'Right'): app.direction = (0, +1)
    # elif (event.key == 's'):
        # this was only here for debugging, before we turned on the timer
        # takeStep(app)

def timerFired(app):
    if app.gameOver or app.waitingForFirstKeyPress: return
    moveWorm(app)
    takeStep(app)

def takeStep(app):
    (drow, dcol) = app.direction
    (wormdrow, wormdcol) = app.wormdirection
    (headwormRow, headwormCol) = app.worm[0]
    (headRow, headCol) = app.snake[0]
    (newwormRow, newwormCol) = (headwormRow+wormdrow, headwormCol + wormdcol)
    (newRow, newCol) = (headRow+drow, headCol+dcol)
    if ((newRow < 0) or (newRow >= app.rows) or
        (newCol < 0) or (newCol >= app.cols) or
        ((newRow, newCol) in app.snake) or
        (newRow, newCol) in app.worm):
        app.gameOver = True
    else:
        app.snake.insert(0, (newRow, newCol))
        if (app.foodPosition == (newRow, newCol)):
            placeFood(app)
        else:
            # didn't eat, so remove old tail (slither forward)
            app.snake.pop()

    #slithers forward worm
    app.worm.insert(0, (newwormRow, newwormCol))
    if (newwormRow, newwormCol) in app.snake:
        app.gameOver = True
    if (newwormRow, newwormCol) == app.foodPosition:
        placeFood(app)
    else:
        app.worm.pop()


def placeFood(app):
    # Keep trying random positions until we find one that is not in
    # the snake. Note: there are more sophisticated ways to do this.
    while True:
        row = random.randint(0, app.rows-1)
        col = random.randint(0, app.cols-1)
        if (row,col) not in app.snake and (row, col) not in app.worm:
            app.foodPosition = (row, col)
            return

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill='white')

def drawSnake(app, canvas):
    for (row, col) in app.snake:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x0, y0, x1, y1, fill='green')

def drawWorm(app, canvas):
    for (row, col) in app.worm:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x0, y0, x1, y1, fill='orange')

def drawFood(app, canvas):
    if (app.foodPosition != None):
        (row, col) = app.foodPosition
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x0, y0, x1, y1, fill='red')

def drawGameOver(app, canvas):
    if (app.gameOver):
        canvas.create_text(app.width/2, app.height/2, text='Game over!',
                           font='Arial 26 bold')
        canvas.create_text(app.width/2, app.height/2+40,
                           text='Press r to restart!',
                           font='Arial 26 bold')

def redrawAll(app, canvas):
    if (app.waitingForFirstKeyPress):
        canvas.create_text(app.width/2, app.height/2,
                           text='Press any key to start!',
                           font='Arial 26 bold')
    else:
        drawBoard(app, canvas)
        drawSnake(app, canvas)
        drawFood(app, canvas)
        drawWorm(app, canvas)
        drawGameOver(app, canvas)


runApp(width=800, height=800)