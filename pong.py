
from cmu_112_graphics import *
#singleplayer pong
def appStarted(app):
    app.waitingForKeyPress = True
    resetApp(app)

def resetApp(app):
    app.timerDelay = 50
    app.dotsLeft = 2
    app.score = 0
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
    app.gameOver = False
    resetDot(app)

def resetDot(app):
    app.dotCx = app.width//2
    app.dotCy = app.height//2
    app.dotDx = -10
    app.dotDy = -3

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

def keyPressed(app, event):
    if app.gameOver:
        resetApp(app)
    elif app.waitingForKeyPress:
        app.waitingForKeyPress = False
        app.dotsLeft -= 1
    elif (event.key == 'Down'):
        movePaddleDown(app)
        movePaddle2Down(app)
    elif (event.key == 'Up'):
        movePaddleUp(app)
        movePaddle2Up(app)

def timerFired(app):
    doStep(app)

def doStep(app):
    if not app.waitingForKeyPress and not app.gameOver:
        moveDot(app)

def dotWentOffEdge(app):
    if app.dotsLeft == 0:
        app.gameOver = True
    else:
        app.waitingForKeyPress = True
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
        app.score += 1 # hurray!
        app.dotDx = -app.dotDx
        app.dotCx = app.paddleX1
        dToMiddleY = app.dotCy - (app.paddleY0 + app.paddleY1)/2
        dampeningFactor = 3 # smaller = more extreme bounces
        app.dotDy = dToMiddleY / dampeningFactor
    elif dotIntersectPaddle2(app):
        app.score += 1 # hurray
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
                       text=f'Score: {app.score}',
                       font=font)
    canvas.create_text(app.width-70, app.height-20,
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

def drawGameOver(app, canvas):
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
    elif app.waitingForKeyPress:
        drawPressAnyKey(app, canvas)
    else:
        drawDot(app, canvas)

def main():
    # This runs the app
    runApp(width=800, height=800)

if __name__ == '__main__':
    main()