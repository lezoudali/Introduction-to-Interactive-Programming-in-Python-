#Please Go to Following link to run the Game
#http://www.codeskulptor.org/#user31_JEEtfrnvwrKmXCH.py

# Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

#deck = Deck()
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize  global variables
in_play = False
outcome = ""
score = 0
prompt = 'Hit or Stand?'

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
       
# define hand class
class Hand:
    def __init__(self):
        #create Hand object
        self.cards = []    
        
    def __str__(self):
        #return a string representation of a hand
        hand = ''
        for card in self.cards:
            hand = hand + card.suit + card.rank + ' '
        return 'Hand contains ' + hand
    
    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand
        value = 0
        ace_flag = False
        for card in self.cards:
            value += VALUES[card.rank]
            if card.rank == 'A':
                ace_flag = True
        if ace_flag:
            if value + 10 > 21:
                return value
            else:
                return value + 10
        else:
            return value
        
# define deck class 
class Deck:
    def __init__(self):
        #pass	# create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(suit+rank)
            
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        deck = ''
        for card in self.deck:
            deck += (card + ' ')
        return 'Deck contains ' + deck

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, prompt, score
    if in_play == True:
        score -=1
    prompt = 'Hit or Stand?'
    outcome = ""
    deck = Deck()
    dealer_hand = Hand()
    player_hand = Hand()
    deck.shuffle()
    card1_str = deck.deal_card()
    card2_str = deck.deal_card()
    card3_str = deck.deal_card()
    card4_str = deck.deal_card()
        
    card1 = Card(card1_str[0], card1_str[1])
    card2 = Card(card2_str[0], card2_str[1])
    card3 = Card(card3_str[0], card3_str[1])
    card4 = Card(card4_str[0], card4_str[1])
        
    player_hand.add_card(card1)
    player_hand.add_card(card3)
    dealer_hand.add_card(card2)
    dealer_hand.add_card(card4)
    in_play = True

def hit():
    global outcome, in_play, score, prompt
    if player_hand.get_value() < 21 and in_play:
        if player_hand.get_value() <= 21:
            card_str = deck.deal_card()
            card = Card(card_str[0], card_str[1])
            player_hand.add_card(card)
        if player_hand.get_value() > 21:
            outcome += "You lose."
            prompt = "New Deal?"
            in_play = False
            score -= 1
       
def stand():
    global outcome, in_play, score, prompt
    if player_hand.get_value() > 21:
        outcome = "You lost."
        in_play = False
        prompt = "New Deal?"
    else:
        if in_play == True:
            while dealer_hand.get_value() < 17:
                card_str = deck.deal_card()
                card = Card(card_str[0], card_str[1])
                dealer_hand.add_card(card)
            if dealer_hand.get_value() <= 21 and dealer_hand.get_value() > player_hand.get_value() and player_hand.get_value() <= 21:
                outcome = "You lose."
                score -= 1
                in_play = False
                prompt = "New Deal?"
            else:
                outcome = "You win."
                score += 1
                in_play = False
                prompt = "New Deal?"

# draw handler    
def draw(canvas):
    global score
    canvas.draw_text("BLACKJACK", (40, 80), 50, 'Navy')
    
    canvas.draw_text(outcome, (200, 150), 20, 'Navy')
    canvas.draw_text("SCORE: " + str(score), (500, 30), 20, 'Red')
    
    x = 50
    canvas.draw_text("Dealer's Hand", (10, 150), 20, 'Black')
    for card in dealer_hand.cards:
        card.draw(canvas, [x, 175])
        x += 100
     
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 175 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
    x = 50   
    canvas.draw_text("Player's Hand", (10,325), 20, 'Black')
    canvas.draw_text(prompt, (200, 325), 20, 'Navy')
    for card in player_hand.cards:
        card.draw(canvas, [x, 350])
        x += 100

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()
frame.start()


