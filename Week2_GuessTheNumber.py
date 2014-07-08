#Please Go to Following link to run the Game
#http://www.codeskulptor.org/#user29_ImjRxns2vL_7.py
#
# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
from random import randrange
from simplegui import create_frame

# initialize global variables used in your code
secret_number, guess, low, high, turns = 0, 0, 0, 100, 6

# helper function to start and restart the game
def new_game():
    # remove this when you add your code 
    global secret_number, low, high, guess
    secret_number = randrange(low, high)
    #print secret_number
    print ''
    print 'NEW GAME'
    print '--------'
    print "Pick a number between " +str(low) + " and " + str(high)
    

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global low, high, turns
    turns = 6
    low, high = 0,  100
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global low, high, turns
    turns = 10
    low, high = 0, 1000
    new_game()
    
def input_guess(inp):
    # main game logic goes here	
    global secret_number, guess, turns
    turns -= 1
    print 'number of turns left:', turns
    guess = int(inp)
    print 'Guess:', guess
    if guess > secret_number and turns:
        print 'Your guess is too high'
        print ''
    elif guess < secret_number and turns:
        print 'Your guess is too low'
        print ''
    elif guess == secret_number and turns:
        print 'Congrats... You guessed the correct number.!!!'
        print ''
        range100()
        print "NEW GAME"
    elif not turns:
        print "Sorry, No turns left!!!" 
        print "The secret number was", secret_number
        new_game()
        
# create frame
frame = create_frame("Guessing Game", 200, 200)

# register event handlers for control elements
frame.add_button("New Game", new_game, 100)
frame.add_button("Range100", range100, 100)
frame.add_button("Range1000", range1000, 100)
frame.add_input('Guess', input_guess, 100)

# call new_game and start frame
new_game()
frame.start()


# always remember to check your completed program against the grading rubric
