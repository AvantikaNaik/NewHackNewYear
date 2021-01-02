inputWord = input("Player 1 give me a word:").lower()

a= 0
while a < 20000:
    a += 1
    print()

def split(word):
    return list(word)

#Code to confirm that it is actually only letters
if (inputWord.isalpha()) == True:
    inputWord = inputWord
else:
    while not (inputWord.isalpha()) == True:
        print("Please enter a valid word")
        inputWord = input("Player 1 give me a word:").lower()

inputWordList = (split(inputWord))

guessWordList = []
for eachIndex in inputWordList:
    guessWordList.append("_")

listLength = len(inputWord)
incorrectlist = []
lives = 7

def guess(lives):
    count = 0
    while (inputWordList != guessWordList) or (lives <= 0):
        guessLetter = input("Player 2, make a guess:").lower()
        if(guessLetter.isalpha() == True and len(guessLetter) == 1):
            print()
        else:
            while not(guessLetter.isalpha() == True and len(guessLetter) == 1):
                print("Please enter a valid guess")
                guessLetter = input("Player 2, make a  guess:").lower()
        for i, letter in enumerate(inputWordList):
            if letter == guessLetter:
                guessWordList[i] = letter
            else:
                count += 1
        if count == listLength:
            lives -= 1
            drawings(lives)
            incorrectlist.append(guessLetter)
            count = 0
        else:
            count = 0

        if lives == 0:
            print("Game Over! You Died!")
            print("Correct Word: " + str(inputWord))
            exit()

        print(guessWordList)
        print("Lives: " + str(lives))
        print("Incorrect Letters: " + str(incorrectlist))
        print()

    print("Yay! You Win! Congrats!")
    print("The word was: " + str(inputWord))

def drawings(lives):
    if lives == 6:
        print ("   ______")
        print ("   |     |")
        print ("   |     o")
        print ("   |     " )
        print ("   |      ")
        print ("   |     " )
        print ("___|_____     ")
    elif lives == 5:
        print ("   ______")
        print ("   |     |")
        print ("   |     o")
        print ("   |   /  " )
        print ("   |     ")
        print ("   |     " )
        print ("___|_____     ")
    elif lives == 4:
        print ("   ______")
        print ("   |     |")
        print ("   |     o")
        print ("   |   / I  " )
        print ("   |     ")
        print ("   |     " )
        print ("___|_____     ")
    elif lives == 3:
        print ("   ______")
        print ("   |     |")
        print ("   |     o")
        print ("   |   / I \ " )
        print ("   |     ")
        print ("   |     " )
        print ("___|_____     ")
    elif lives == 2:
        print ("   ______")
        print ("   |     |")
        print ("   |     o")
        print ("   |   / I \ " )
        print ("   |     I")
        print ("   |     " )
        print ("___|_____     ")
    elif lives == 1:
        print ("   ______")
        print ("   |     |")
        print ("   |     o")
        print ("   |   / I \ " )
        print ("   |     I")
        print ("   |    /   " )
        print ("___|_____     ")
        print ("one last chance")
    elif lives == 0:
        print ("   ______")
        print ("   |     |")
        print ("   |     o")
        print ("   |   / I \ " )
        print ("   |     I")
        print ("   |    /  \ " )
        print ("___|_____     ")


guess(lives)
