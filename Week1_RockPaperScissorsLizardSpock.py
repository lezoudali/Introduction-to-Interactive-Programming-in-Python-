#Please Go to Following link to run the Game
#http://www.codeskulptor.org/#user35_wAaL9IjFt1rA3c9.py
#
# Rock-paper-scissors-lizard-Spock template
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

from random import randrange

def name_to_number(name):
    
    case = dict(zip(["rock", "spock", "paper", "lizard", "scissors"], [0, 1, 2, 3, 4]))
    return case[name.lower()]

def number_to_name(number):
    
    case = dict(zip([0, 1, 2, 3, 4], ["rock", "Spock", "paper", "lizard", "scissors"]))
    return case[number]

def rpsls(player_choice): 

    print 'Player chooses ' + player_choice       # print out the message for the player's choice
    player_number = name_to_number(player_choice) # convert the player's choice to player_number using the function name_to_number()
    comp_number = randrange(0,5)           # compute random guess for comp_number using random.randrange()
    comp_choice = number_to_name(comp_number)     # convert comp_number to comp_choice using the function number_to_name()
    print 'Computer chooses ' + comp_choice       # print out the message for computer's choice
    diff = (player_number - comp_number)%5        # compute difference of comp_number and player_number modulo five
    winner = "Player and computer tie!"
    if diff:
        winner = 'Player wins!' if (diff == 1 or diff == 2) else 'Computer wins!' # use if/elif/else to determine winner, print winner message
    print winner 
    print '' 									  # print new line between games
    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


