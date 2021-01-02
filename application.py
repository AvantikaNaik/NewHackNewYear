##############################################
#New Year New Hack
#Jackbox Minigames
##############################################

from cmu_112_graphics import *
import random
import time

# War Stuff

import sys
from cards import Player
from cards import Deck
from cards import Card
sys.path.append('war')
from war import War

######################
#Snake Stuff
#####################
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
##############################################
# General Purpose Helper Functions
##############################################

def getCell(app, x, y):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y - app.margin) // cellHeight)
    col = int((x - app.margin) // cellWidth)
    return (row, col)

def getCellBounds(app, row, col):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)


def playWar(app):
    players = []

    print("LET'S PLAY WAR! \nENTER PLAYERS SEPERATED WITH COMMAS:")
    namestr = input()
    for name in namestr.split(", "):
        players.append(Player(name))
    print("HERE ARE YOUR PLAYERS:")
    for player in players:
        print(player.name)


    game = War(players)
    while len(players[0].hand) > 0:
        nextMove = input("Enter 'move' to make the next move, enter 'hands' to check how many cards are in each player's hands,\n or enter 'piles' to see how many cards are in each player's piles.\n")
        if nextMove == "move":
            game.playRound()
        elif nextMove == "hands":
            for player in players:
                print(player.name + " has " + str(len(player.hand)) + " cards left.")
        elif nextMove == "piles":
            for player in players:
                print(player.name + " has " + str(len(player.pile)) + " cards in their discard pile.")
        else:
            print("Not a valid move")
        print("\n\n\n")
    print("Here are the winners: ")
    for player in game.winners():
        print(player.name + " with " + str(len(player.pile)) + " cards in their pile.")
        app.playerName = player.name
        app.playerPile = player.pile
    app.showingWarWinner = True
    app.warMode = False

def playSnake(app):
    if app.gameOver or app.waitingForFirstKeyPress: return
    moveWorm(app)
    takeStep(app)

##############################################
#App Stuff
##############################################
def appStarted(app):
    app.titleScreenShowing = True
    app.titleScreenCounter = 0

    app.gameMenuAnimation = False
    app.gameMenuAnimationCounter = 0

    app.gamesShowing = False

    app.hangmanMode = False
    app.snakeMode = False
    app.skribbleMode = False
    app.warMode = False

    #War Varaibles
    app.showingWarWinner = False
    app.playerName = ""
    app.playerPile = ""
    app.warWinnerCounter = 0

    #Snake Variables
    app.rows = 20
    app.cols = 20
    app.margin = 5 # margin around grid
    app.timerDelay = 250
    initSnakeAndWormAndFood(app)
    app.waitingForFirstKeyPress = True
    app.showSnakeModeOptions = False
    app.aiSnakeMode = False
    app.multiplayerSnakeMode = False
    app.gameOverCounter = 0 

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


def timerFired(app):
    app.titleScreenCounter += 1
    app.gameMenuAnimationCounter += 1
    if app.titleScreenCounter > 20:
        app.titleScreenShowing = False
    if not app.titleScreenShowing:
        app.gameMenuAnimation = True
        app.gamesShowing = True
    if app.gameMenuAnimationCounter > 27:
        app.gameMenuAnimation = False
    if app.warMode:
        playWar(app)
    if app.showingWarWinner:
        app.warWinnerCounter += 1
    if app.warWinnerCounter > 20:
        app.showingWarWinner = False
    if app.snakeMode and not (app.aiSnakeMode or app.multiplayerSnakeMode):
        app.showSnakeModeOptions = True
    if app.snakeMode and app.aiSnakeMode:
        playSnake(app)
    if app.snakeMode and app.gameOver:
        app.gameOverCounter += 1
    if app.gameOverCounter > 10:
        initSnakeAndWormAndFood(app)
        app.aiSnakeMode = False
        app.snakeMode = False
        app.gameOverCounter = 0

def mousePressed(app, event):
    xMargin = app.width//25
    yMargin = app.height//25
    
    if app.gamesShowing and not app.gameMenuAnimation and not app.showSnakeModeOptions and not app.snakeMode:
        if (xMargin < event.x < app.width//2-xMargin) and (yMargin < event.y < app.height//2 - yMargin):
            app.hangmanMode = True
            print("hangman")
        elif (xMargin < event.x < app.width//2-xMargin) and (app.height//2 + yMargin < event.y < app.height - yMargin):
            app.warMode = True
        elif (app.width//2 + xMargin < event.x < app.width-xMargin) and (yMargin < event.y < app.height//2 - yMargin):
            app.skribbleMode = True
            print("skribble")
        elif (app.width//2 + xMargin < event.x < app.width-xMargin) and (app.height//2 + yMargin < event.y < app.height - yMargin): 
            app.snakeMode = True
    if app.showSnakeModeOptions:
        if 0 < event.x < app.width//2:
            initSnakeAndWormAndFood(app)
            app.waitingForFirstKeyPress = True
            app.showSnakeModeOptions = False
            app.gameOverCounter = 0
            app.aiSnakeMode = True
        else: 
            app.multiplayerSnakeMode = True
            app.showSnakeModeOptions = False

def keyPressed(app, event):
    if app.snakeMode:
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

##############################################
#Drawing Stuff
##############################################
def drawTitleScreen(app, canvas):
    canvas.create_text(app.width//2, app.height//4, fill="white", text="Welcome to", font="Arial 40 bold")
    canvas.create_text(app.width//2, app.height//2, fill="white", text="*INSERT NAME HERE*", font="Arial 55 bold")
    canvas.create_text(app.width//2, 3 * app.height//4, fill="white", text="A cool and interesting subtitle", font="Arial 40 bold")

def drawGameMenuAnimation(app, canvas):
    canvas.create_text(app.width//2, app.height//2, fill="black", text="OUR GAMES...", font="Arial 55 bold")

def drawGames(app, canvas):
    xMargin = app.width//25
    yMargin = app.height//25
    canvas.create_rectangle(xMargin, yMargin, app.width//2-xMargin, app.height//2 - yMargin, fill="white")
    canvas.create_rectangle(xMargin, app.height//2 + yMargin, app.width//2-xMargin, app.height - yMargin, fill="white")
    canvas.create_rectangle(app.width//2 + xMargin, yMargin, app.width-xMargin, app.height//2 - yMargin, fill="white")
    canvas.create_rectangle(app.width//2 + xMargin, app.height//2 + yMargin, app.width-xMargin, app.height - yMargin, fill="white")
    drawHangman(app, canvas, xMargin, yMargin, app.width//2-xMargin, app.height//2 - yMargin)
    drawWar(app, canvas, xMargin, app.height//2 + yMargin, app.width//2-xMargin, app.height - yMargin)
    drawSkribble(app, canvas, app.width//2 + xMargin, yMargin, app.width-xMargin, app.height//2 - yMargin)
    drawSnakeArt(app, canvas, app.width//2 + xMargin, app.height//2 + yMargin, app.width-xMargin, app.height - yMargin)

def drawHangman(app, canvas, x1, y1, x2, y2):
    gridWidth = x2 - x1
    gridHeight = y2 - y1
    midX = (x2 + x1)//2
    midY = (y2 + y1)//2

    canvas.create_oval(midX - gridWidth//8, y1 + gridWidth//12, midX + gridWidth//8, y1 + gridWidth//12 + 2 * gridWidth//8, outline="black", width="5" )
    canvas.create_line(midX, y1 + gridWidth//12 + 2 * gridWidth//8, midX,  midY + gridHeight//8, width=7, fill="black")
    canvas.create_line(midX - gridWidth//8, midY, midX + gridWidth//8, midY, width=7, fill="black")
    canvas.create_line(midX, midY + gridHeight//8, midX - gridWidth//8, y2 - gridHeight//8, width=7, fill="black" )
    canvas.create_line(midX, midY + gridHeight//8, midX + gridWidth//8, y2 - gridHeight//8, width=7, fill="black" )
    canvas.create_text(midX, y2 - gridHeight//16, text="Hangman")

def drawWar(app, canvas, x1, y1, x2, y2):
    gridWidth = x2 - x1
    gridHeight = y2 - y1
    midX = (x2 + x1)//2
    midY = (y2 + y1)//2
    
    canvas.create_rectangle(x1 + gridWidth//4, y1 + gridHeight//7, x2 - gridWidth//4, y2 - gridHeight//7, width=3)
    canvas.create_text(x1 + gridWidth//4 + gridWidth//25, y1 + gridHeight//7 + gridWidth//25, text="A", fill="red", font="30")
    canvas.create_text(x2 - gridWidth//4 - gridWidth//25, y2 - gridHeight//7 - gridWidth//25, text="A", fill="red", font="30")
    canvas.create_polygon(midX, midY+gridHeight//7, midX-gridHeight//8, midY, midX, midY - gridHeight//7, midX+gridHeight//8, midY, fill="red")
    canvas.create_text(midX, y2 - gridHeight//16, text="War")

def drawSkribble(app, canvas, x1, y1, x2, y2):
    gridWidth = x2 - x1
    gridHeight = y2 - y1
    midX = (x2 + x1)//2
    midY = (y2 + y1)//2

    canvas.create_rectangle(midX - gridWidth//8, y1 + gridWidth//12, midX + gridWidth//8, y1 + gridWidth//6, outline="black", width="3", fill="pink" )
    canvas.create_rectangle(midX - gridWidth//8, y1 + gridWidth//6, midX + gridWidth//8, midY + gridWidth//6, outline="black", width="3", fill="yellow" )
    canvas.create_line(midX - gridWidth//8 + gridWidth//12, y1 + gridWidth//6, midX - gridWidth//8 + gridWidth//12, midY + gridWidth//6, fill="black", width="3")
    canvas.create_line(midX - gridWidth//8 + gridWidth//6, y1 + gridWidth//6, midX - gridWidth//8 + gridWidth//6, midY + gridWidth//6, fill="black", width="3")
    canvas.create_polygon(midX - gridWidth//8, midY + gridWidth//6, midX + gridWidth//8, midY + gridWidth//6, midX, y2-gridHeight//6, fill="PeachPuff2", width=3, outline="black")
    canvas.create_polygon(midX - gridWidth//16, y2- 3 * (gridHeight//12), midX + gridWidth//16,  y2- 3 * (gridHeight//12), midX, y2-gridHeight//6, fill="black", width=3, outline="black")
    canvas.create_text(midX, y2 - gridHeight//16, text="Skribble")

def drawSnakeArt(app, canvas, x1, y1, x2, y2):
    gridWidth = x2 - x1
    gridHeight = y2 - y1
    midX = (x2 + x1)//2
    midY = (y2 + y1)//2
    yMargin = gridHeight//7

    canvas.create_rectangle(midX-gridWidth//3, y1 + yMargin , midX+gridWidth//3, y1+ (2 * yMargin), fill="green", width=0)
    canvas.create_rectangle(midX-gridWidth//3, y1+ (2 * yMargin), midX-gridWidth//3 + yMargin, y1 + (3 * yMargin), fill="green", width=0)
    canvas.create_rectangle(midX-gridWidth//3, y1 + (3 * yMargin), midX+gridWidth//3, y1 + (4 * yMargin), fill="green", width=0)
    canvas.create_rectangle(midX+gridWidth//3 - yMargin, y1 + (4 * yMargin), midX+gridWidth//3, y1 + (5 * yMargin), fill="green", width=0)
    canvas.create_rectangle(midX-gridWidth//3, y1 + (5 * yMargin), midX+gridWidth//3, y1+ (6 * yMargin), fill="green", width=0)
    eyeOffset = gridWidth//30
    canvas.create_oval(midX+gridWidth//3 - gridHeight//7+5, y1+yMargin + 5, midX+gridWidth//3 - gridHeight//7+2*eyeOffset, y1+yMargin + 2*eyeOffset, fill="gray")
    canvas.create_text(midX, y2 - gridHeight//16, text="Snake")


def drawCard(app, canvas, rank, suit):
    pass

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
        canvas.create_rectangle(0, 0, app.width, app.height, fill="pink")
        canvas.create_text(app.width/2, app.height/2, text='Game over!',
                           font='Arial 26 bold')

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="pink")
    if app.titleScreenShowing:
        canvas.create_rectangle(0, 0, app.width, app.height, fill="purple")
        drawTitleScreen(app, canvas)
    if app.gameMenuAnimation: 
        drawGameMenuAnimation(app, canvas)
    if app.gamesShowing:
        drawGames(app, canvas)
    if app.warMode:
        canvas.create_rectangle(0, 0, app.width, app.height, fill="pink")
        canvas.create_text(app.width//2, app.height//4, text="War is an n-player game!", font="Arial 30 bold")
        canvas.create_text(app.width//2, 2 * app.height//4, text="Play it in your terminal!", font="Arial 30 bold")
        drawWar(app, canvas, app.width//4, app.height//2, 3 * app.width//4, 15 * app.height//16)
    if app.showingWarWinner:
        canvas.create_rectangle(0, 0, app.width, app.height, fill="pink")
        canvas.create_text(app.width//2, app.height//4, text="Congrats! The winner is", font="Arial 30 bold")
        canvas.create_text(app.width//2, 2 * app.height//4, text=f"{str(app.playerName)} with {str(len(app.playerPile))} cards!", font="Arial 30 bold")
    if app.gameOver:
        drawGameOver(app, canvas)
    if app.snakeMode and not app.gameOver:
        if (app.waitingForFirstKeyPress):
            canvas.create_rectangle(0, 0, app.width, app.height, fill="pink")
            canvas.create_text(app.width/2, app.height/2,
                            text='Press any key to start AI snake!',
                            font='Arial 26 bold')
        else:
            drawBoard(app, canvas)
            drawSnake(app, canvas)
            drawFood(app, canvas)
            drawWorm(app, canvas)
            drawGameOver(app, canvas)
    if app.showSnakeModeOptions and not app.gameOver:
        canvas.create_rectangle(0, 0, app.width//2, app.height, fill="pink")
        canvas.create_text(app.width/4, app.height//2,
                            text='AI snake!',
                            font='Arial 26 bold')
        canvas.create_rectangle(app.width//2, 0, app.width, app.height, fill="light green")
        canvas.create_text(3 * app.width//4, app.height//2,
                            text='Multiplayer Snake!',
                            font='Arial 26 bold')
##############################################
# Run App
##############################################
runApp(width=800, height=800)

if __name__ == '__main__':
    main()

