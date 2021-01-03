from cmu_112_graphics import *
from random_words import RandomWords
rw = RandomWords()

def appStarted(app):
    app.word = rw.random_word()
    print(app.word)
    app.guessedLetters = set()
    app.currentList = []
    generateLists(app)
    app.textbox = "..."
    app.journalEntry = False

    app.win = False
    app.lose = False
    app.bodyParts = 0

def generateLists(app):
    listLen = len(app.word)
    app.currentList = []
    app.wordList = list(app.word)
    for i in range(len(app.word)):
        app.currentList.append("_")

def timerFired(app):
    if app.wordList == app.currentList:
        app.win = True
    if app.bodyParts == 6:
        app.lose = True
    if app.currentList == app.wordList:
        app.win == True
    
def keyPressed(app, event):
    if app.journalEntry:
        if app.textbox == "...":
            app.textbox = ""
        if event.key == "Enter" or event.key == "Escape":
            app.journalEntry = not app.journalEntry
        if event.key == "Backspace":
            endVal = len(app.textbox)
            if endVal != 0:
                app.textbox = app.textbox[:endVal-1]
            else:
                app.textbox = ""
        elif event.key == "Space":
            app.textbox += " "
        elif event.key in {"Up", "Down", "Left","Right"}:
            app.textbox += "" 
        elif event.key not in {"Backspace", "Enter", "Escape"}:
            app.textbox += event.key
    else: 
        if event.key == "Enter":
            app.guessedLetters.add
            checkGuess(app, app.textbox)
            app.textbox = "..."

def checkGuess(app, letter):
    if len(letter) != 1:
        app.bodyParts += 1
    elif letter not in app.wordList:
        app.bodyParts += 1
        app.guessedLetters.add(letter)
    else: 
        for i, wordLetter in enumerate(app.wordList):
            if letter == wordLetter:
                app.currentList[i] = app.wordList[i]
            
def mousePressed(app, event):
    if app.width//4 < event.x < 3*app.width//4 and 3 * app.height//4 < event.y < 15 * app.height//16:
        app.journalEntry = True
    else: app.journalEntry = False

def drawTextBox(app, canvas):
    if app.journalEntry: fill="pink"
    else: fill="white"
    canvas.create_rectangle(app.width//4, 3 * app.height//4, 3*app.width//4, 15 * app.height//16, fill=fill)
    canvas.create_text(app.width//2, 7 * app.height//8, text=app.textbox)

def drawNoose(app, canvas):
    x = app.width//20
    canvas.create_line(2*x, 2 * x, 2 *x, 8 * x, width=5)
    canvas.create_line(2 *x, 2 * x,6*x, 2*x, width=5)
    canvas.create_line(2*x, 2 * x, 2*x, 10 * x, width=5)
    canvas.create_line(x, 10*x, 3 * x,10*x, width=5)
    canvas.create_line(6 *x, 4 * x, 6 * x, 2*x, width=5)

def drawBlanks(app, canvas):
    numBlanks = len(app.word)
    lenBlanks = (7 * app.width//10) // numBlanks - 20
    canvas.create_text(6.5 * app.width//10, 2 * app.width//10, text=app.currentList, font = f"Arial {lenBlanks}")

def guesses(app, canvas):
    canvas.create_text(app.width//2, 2 * app.height//3, text = f"Guessed Letters: {app.guessedLetters}")

def drawUsage(app, canvas):
    canvas.create_text(app.width//2, 23 * app.height//24, text = "Once you type a letter, exit the text box and hit enter to submit the letter" )

def drawHead(app, canvas):
    x = app.width//20
    canvas.create_oval(5 * x, 4* x, 7*x, 6*x)

def drawBody(app, canvas):
    x = app.width//20
    canvas.create_line(6 * x, 6*x, 6*x, 8*x)

def drawLeftArm(app, canvas):
    x = app.width//20
    canvas.create_line(6 * x, 7*x, 5*x, 7*x)

def drawRightArm(app, canvas):
    x = app.width//20
    canvas.create_line(6 * x, 7*x, 7*x, 7*x)

def drawLeftLeft(app, canvas):
    x = app.width//20
    canvas.create_line(6 * x, 8*x, 5*x, 10*x)

def drawRightLeg(app, canvas):
    x = app.width//20
    canvas.create_line(6 * x, 8*x, 7*x, 10*x)



def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height)
    drawTextBox(app, canvas)
    drawNoose(app, canvas)
    drawBlanks(app, canvas)
    guesses(app, canvas)
    drawUsage(app, canvas)
    if app.win:
        canvas.create_text(app.width//2, app.height//2, text="You Win!")
    if app.lose:
        canvas.create_text(app.width//2, app.height//2, text="You Lost!")
    if app.bodyParts == 1:
        drawHead(app, canvas)
    elif app.bodyParts == 2:
        drawHead(app, canvas)
        drawBody(app, canvas)
    elif app.bodyParts == 3:
        drawHead(app, canvas)
        drawBody(app, canvas)
        drawLeftArm(app, canvas)
    elif app.bodyParts == 4:
        drawHead(app, canvas)
        drawBody(app, canvas)
        drawLeftArm(app, canvas)
        drawRightArm(app, canvas)
    elif app.bodyParts == 5:
        drawHead(app, canvas)
        drawBody(app, canvas)
        drawLeftArm(app, canvas)
        drawRightArm(app, canvas)
        drawLeftLeft(app, canvas)
    elif app.bodyParts == 6:
        drawHead(app, canvas)
        drawBody(app, canvas)
        drawLeftArm(app, canvas)
        drawRightArm(app, canvas)
        drawLeftLeft(app, canvas)
        drawRightLeg(app, canvas)
runApp(width=800, height=800)