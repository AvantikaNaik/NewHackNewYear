##############################################
#New Year New Hack
#Jackbox Minigames
##############################################

from cmu_112_graphics import *
import random
import time


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



def timerFired(app):
    app.titleScreenCounter += 1
    app.gameMenuAnimationCounter += 1
    if app.titleScreenCounter > 30:
        app.titleScreenShowing = False
    if not app.titleScreenShowing:
        app.gameMenuAnimation = True
        app.gamesShowing = True
    if app.gameMenuAnimationCounter > 50:
        app.gameMenuAnimation = False


def mousePressed(app, event):
    xMargin = app.width//25
    yMargin = app.height//25
    
    if app.gamesShowing and not app.gameMenuAnimation:
        if (xMargin < event.x < app.width//2-xMargin) and (yMargin < event.y < app.height//2 - yMargin):
            app.hangmanMode = True
            print("hangman")
        elif (xMargin < event.x < app.width//2-xMargin) and (app.height//2 + yMargin < event.y < app.height - yMargin):
            app.warMode = True
            print("war")
        elif (app.width//2 + xMargin < event.x < app.width-xMargin) and (yMargin < event.y < app.height//2 - yMargin):
            app.skribbleMode = True
            print("skribble")
        elif (app.width//2 + xMargin < event.x < app.width-xMargin) and (app.height//2 + yMargin < event.y < app.height - yMargin): 
            app.snakeMode = True
            print("snake")
def keyPressed(app, event):
    pass


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
    drawSnake(app, canvas, app.width//2 + xMargin, app.height//2 + yMargin, app.width-xMargin, app.height - yMargin)

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

def drawSnake(app, canvas, x1, y1, x2, y2):
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


def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="pink")
    if app.titleScreenShowing:
        canvas.create_rectangle(0, 0, app.width, app.height, fill="purple")
        drawTitleScreen(app, canvas)
    if app.gameMenuAnimation: 
        drawGameMenuAnimation(app, canvas)
    if app.gamesShowing:
        drawGames(app, canvas)
    
##############################################
# Run App
##############################################
runApp(width=800, height=800)

if __name__ == '__main__':
    main()

