#Please Go to Following link to run the Game
#http://www.codeskulptor.org/#user31_Ue685drffiT59r3.py
#
# implementation of card game - Memory

import simplegui
import random
state, prev1, prev2, turns= 0, None, None, 0
# helper function to initialize globals

def new_game():
    global cards, exposed, state, turns
    exposed, cards, state, turns, prev1, prev2 = [False for x in range(16)], range(8) + range(8), 0, 0, None, None
    random.shuffle(cards)
    label.set_text("Turns = "+str(turns))
    #print cards
     
#event handlers
def mouseclick(pos):
    global state, prev1, prev2 , turns, cards
    
    #game state logic
    card, pos = 0, list(pos)
    for i in range(49, 800, 50):    
        if pos[0] < i :
            if exposed[card] == True:
                break
            else:
                exposed[card] = True
            if state == 0:
                state = 1 
                turns += 1
                label.set_text("Turns = "+str(turns))
                prev1 = card
            elif state == 1:
                state = 2
                prev2 = card
            else: 
                state = 1
                turns += 1
                label.set_text("Turns = "+str(turns))
                if cards[prev1] != cards[prev2]:
                    exposed[prev1] = False
                    exposed[prev2] = False 
                prev1 = card
                prev2 = None
            break
        card +=1
                                     
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards; card_pos = 7.5; x = 0
    for c in cards:
        canvas.draw_text(str(c), (card_pos, 70), 70, 'white')
        card_pos += 50
   
    for i in range(16):
        if exposed[i]:
            canvas.draw_polygon([[x,0], [x, 100], [49+x, 100], [49+x, 0]], 1, 'black')
            x = x + 50
        else: 
            canvas.draw_polygon([[x,0], [x, 100], [49+x, 100], [49+x, 0]], 1, 'black','red')
            x = x + 50
     
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric