
from cmu_112_graphics import *
import random
#singleplayer pong
def appStarted(app):
    app.waitingForKeyPressPong = True
    resetApp(app)

def resetApp(app):
    app.timerDelay = 50
    app.dotsLeft = 5
    app.leftScore = 0
    app.rightScore = 0
    app.paddleX0 = 20
    app.paddleX1 = 40
    app.paddleY0 = 20
    app.paddleY1 = 100

    app.paddle2X0 = app.width - 20
    app.paddle2X1 = app.width - 40
    app.paddle2Y0 = 20
    app.paddle2Y1 = 100

    app.margin = 5
    app.paddleSpeed = 10
    app.dotR = 15
    app.gameOverPong = False
    resetDot(app)

def resetDot(app):
    app.dotCx = app.width//2
    app.dotCy = app.height//2
    i = random.randint(1, 4)
    app.dotDx = -10 * ((-1)**i)
    app.dotDy = -3 * ((-1)**i)
    app.timer = 0

def movePaddleDown(app):
    dy = min(app.paddleSpeed, app.height - app.margin - app.paddleY1)
    app.paddleY0 += dy
    app.paddleY1 += dy

def movePaddle2Down(app):
    dy = min(app.paddleSpeed, app.height - app.margin - app.paddle2Y1)
    app.paddle2Y0 += dy
    app.paddle2Y1 += dy

def movePaddleUp(app):
    dy = min(app.paddleSpeed, app.paddleY0 - app.margin)
    app.paddleY0 -= dy
    app.paddleY1 -= dy

def movePaddle2Up(app):
    dy = min(app.paddleSpeed, app.paddle2Y0 - app.margin)
    app.paddle2Y0 -= dy
    app.paddle2Y1 -= dy

def moveAIPaddle(app):
    paddleMid = (app.paddle2Y0 + app.paddle2Y1)//2
    offset = random.randint(1, 28)
    offset2 = random.randint(1, 28)
    if app.dotCy <= paddleMid - offset:
        movePaddle2Up(app)
    if app.dotCy > paddleMid + offset2:
        movePaddle2Down(app)

def keyPressed(app, event):
    if app.gameOverPong:
        resetApp(app)
    elif app.waitingForKeyPressPong:
        app.waitingForKeyPressPong = False
        app.dotsLeft -= 1
    elif (event.key == 'Down'):
        movePaddleDown(app)
    elif (event.key == 'Up'):
        movePaddleUp(app)

def timerFired(app):
    if not app.waitingForKeyPressPong and not app.gameOverPong:
        moveDot(app)
        moveAIPaddle(app)
        app.timer += 1
        if app.timer > 50:
            app.timerDelay -= 1
            app.timer = 0

def dotWentOffEdge(app):
    if app.dotsLeft == 0:
        app.gameOverPong = True
    else:
        app.waitingForKeyPressPong = True
        resetDot(app)

def dotIntersectsPaddle(app):
    return ((app.paddleX0 <= app.dotCx <= app.paddleX1) and
            (app.paddleY0 <= app.dotCy <= app.paddleY1))

def dotIntersectPaddle2(app):
    return ((app.paddle2X1 <= app.dotCx <= app.paddle2X0) and
            (app.paddle2Y0 <= app.dotCy <= app.paddle2Y1))

def moveDot(app):
    app.dotCx += app.dotDx
    app.dotCy += app.dotDy
    if (app.dotCy + app.dotR >= app.height):
        # The dot went off the bottom!
        app.dotCy = app.height - app.dotR
        app.dotDy = -app.dotDy
    elif (app.dotCy - app.dotR <= 0):
        # The dot went off the top!
        app.dotCy = app.dotR
        app.dotDy = -app.dotDy
    elif dotIntersectsPaddle(app):
        # The dot hit the paddle!
        app.leftScore += 1 # hurray!
        app.dotDx = -app.dotDx
        app.dotCx = app.paddleX1
        dToMiddleY = app.dotCy - (app.paddleY0 + app.paddleY1)/2
        dampeningFactor = 3 # smaller = more extreme bounces
        app.dotDy = dToMiddleY / dampeningFactor
    elif dotIntersectPaddle2(app):
        app.rightScore += 1 
        app.dotDx = -app.dotDx
        app.dotCx = app.paddle2X1
        dToMiddleY = app.dotCy - (app.paddle2Y0 + app.paddle2Y1)/2
        dampeningFactor = 3 # smaller = more extreme bounces
        app.dotDy = dToMiddleY / dampeningFactor
    elif (app.dotCx - app.dotR <= 0) or (app.dotCx + app.dotR >= app.width):
        # The dot went off the left side
        dotWentOffEdge(app)

def drawAppInfo(app, canvas):
    font = 'Arial 18 bold'
    canvas.create_text(app.width-70, 20,
                       text=f'Score: {app.rightScore}',
                       font=font)
    canvas.create_text(70, 20,
                        text=f'Score: {app.leftScore}',
                        font=font)
    canvas.create_text(app.width//2, app.height-20,
                       text=f'Dots Left: {app.dotsLeft}',
                       font=font)

def drawPaddle(app, canvas):
    # This is a helper function for the View
    canvas.create_rectangle(app.paddleX0, app.paddleY0,
                            app.paddleX1, app.paddleY1,
                            fill='black')

def drawPaddle2(app, canvas):
    canvas.create_rectangle(app.paddle2X0, app.paddle2Y0,
                                app.paddle2X1, app.paddle2Y1,
                                fill='black')

def drawDot(app, canvas):
    # This is a helper function for the View
    cx, cy, r = app.dotCx, app.dotCy, app.dotR
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='black')

def drawGameOverPong(app, canvas):
    # This is a helper function for the View
    canvas.create_text(app.width/2, app.height/2,
                       text='Game Over!',
                       font='Arial 18 bold')
    canvas.create_text(app.width/2, app.height/2 + 50,
                       text='Press any key to restart',
                       font='Arial 16 bold')

def drawPressAnyKey(app, canvas):
    # This is a helper function for the View
    canvas.create_text(app.width/2, app.height/2,
                       text='Press any key to start!',
                       font='Arial 18 bold')

def redrawAll(app, canvas):
    # This is the View
    drawAppInfo(app, canvas)
    drawPaddle(app, canvas)
    drawPaddle2(app, canvas)
    if app.gameOver:
        drawGameOver(app, canvas)
    elif app.waitingForKeyPressPong:
        drawPressAnyKey(app, canvas)
    else:
        drawDot(app, canvas)

def main():
    # This runs the app
    runApp(width=800, height=800)

if __name__ == '__main__':
    main()