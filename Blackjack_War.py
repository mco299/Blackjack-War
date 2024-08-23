# Blackjack War
# This is a recreation of the game Blackjack with a twist using OOP.

# ------------------------------------Rules------------------------------------
# The Players:
# In Blackjack, a Player plays against the Dealer (the computer in this case).
# This version contains no gambling. The Player either wins or loses. They do not try to conserve
# or win money.
# This version is almost the same as regular Blackjack, except there's no splitting, all of the
# Dealer's cards are always visible, and there's a twist that occurs if the Player and Dealer tie,
# which breaks the tie.

# Gameplay:
# To start, the Dealer deals cards to both the Player and itself.
# The Player can decide to "Stay" or ask the Dealer to "Hit Me."
# If the Player decides to ask the Dealer to hit them, the Dealer deals them an additional card.
# The Dealer decides whether or not to deal for itself (see Busting).
# For every card dealt, the value of the Player and Dealer's Hands increases depending on the card
# dealt (see Card Values). Once the Player or the Dealer decide to "Stay" the value of their Hand
# is locked in.
# In order to win, the Player must have a Hand with a value greater than the Dealer's, but not
# greater than 21 (see Busting). Essentially, whoever's Hand is closest to 21 determines whether
# or not the Player wins.

# Busting:
# If either the Player or the Dealer have a Hand after dealing with a value greater than 21, that
# person "Busts," meaning the value of their Hand becomes worthless.
# If the Dealer Busts before the Player, the Player automatically wins. If the Player Busts, the
# Player automatically loses. If both Bust at the same time, the Player still loses.
# The Dealer will automatically Hit if the value of their cards is 16 or below. They automatically
# Stay if their cards are worth 17 or higher.

# Tie:
# A Hand with a value that is exactly 21 is called a Blackjack.
# If both the Player and the Dealer end up with a Blackjack or tie, the Dealer will draw a
# card for the both of them. If the Player has a card that is greater than the Dealer's, the
# Player wins. If less, the Player loses.
# If they tie again, The suit of the cards determines whether a card's higher or lower to break
# ties as much as possible (see Card Suits). So whether the Player wins at this point or not is
# entirely up to Chance.
# The value of an Ace is automatically 11 under this condition (see Card Values).

# Card Values:
# The value of a Number Card is equal to itself (2 = 2, 3 = 3, etc.).
# The value of a Face Card (Ace, Jack, Queen, King) is shown below:
# Ace = 1 or 11 (depending on the situation, see The Ace Card)
# Jack = 10
# Queen = 10
# King = 10

# Card Suits:
# In the case of a tie, these are the order of the suits:
# Clubs < Diamonds < Hearts < Spades
# For example, if the Player has a 2 of Diamonds and the Dealer a 2 of Spades, the Player loses.

# The Ace Card:
# The Ace Card is special in that it has 2 possible values.
# Its value is 11 by default if it doesn't cause a Bust. If it does cause a Bust, its value is 1.
# If the Player has an Ace worth 11 in their Hand already and then Busts, the value of that Ace
# changes to 1 to avoid Busting. If, in that case, the Player's hand decreases so that it is no
# longer a Bust, the Player can continue playing as normal until they win or actually Bust.
# All these conditions also apply to the Dealer.

class Card:
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_list = ["None","Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    # "None" is a dummy variable because we want "Ace" and onwards to be at those indexes
    def __init__(self, suit = 0, rank = 2):
        self.suit = suit
        self.rank = rank
    def __str__(self): # overwrites print function; returns the card
        return self.rank_list[self.rank] + " of " + self.suit_list[self.suit]
    def __eq__(self, other): # returns whether the cards are equal or not, in just rank
        return (self.rank == other.rank) # and self.suit == other.suit)
    # we want the suit to be more important than rank when comparing
    def __gt__(self, other): # checks if a card is greater than the other
        if self.rank > other.rank: # if rank of this card is greater, return True
            return True
        elif self.rank == other.rank: # if ranks are equal check suit
            if self.suit > other.suit:
                return True
        return False

import random
import math

class Deck():
    def __init__(self): # creates standard 52 Deck using class Card
        self.cards = []
        for suit in range(4): # 0, 1, 2, 3
            for rank in range(1,14):
                self.cards.append(Card(suit, rank))
    def __str__(self): # list all cards in Deck
        s = ""
        for i in range(len(self.cards)):
            s += i * " " + str(self.cards[i]) + "\n"
        return s
    def shuffle(self): # shuffles Deck
        n_cards = len(self.cards)
        for i in range(n_cards):
            j = random.randrange(0, n_cards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
            # card i becomes card j and card j becomes card i
    def pop_card(self): # removes a card from the Deck
        return self.cards.pop()
    def is_empty(self): # checks if Deck is empty
        return len(self.cards) == 0
    def deal(self, hands, n_cards): # hands is a list of players
        n_players = len(hands)
        for i in range(n_cards):
            if self.is_empty():
                break
            card = self.pop_card()
            current_player = i % n_players
            # dividing by the number of players; remainder division
            hands[current_player].add_card(card) # .add_card is defined in class Hand

class Hand(Deck): # Hand inherits values from Deck
    def __init__(self, name = "The Dealer"): # The Dealer is called by default
        self.cards = []
        self.name = name
        self.v = [] # add a list of values
        self.stay = 0
    def add_card(self, card):
        self.cards.append(card) # used in line 115 in Deck.deal()
        # add card rank to Hand; Ace is 11 by default
        if card.rank == 1: # if an Ace
            self.v.append(11) # default is 11
        elif (card.rank == 11) or (card.rank == 12) or (card.rank == 13):
            self.v.append(10) # if Jack, Queen, or King
        else:
            self.v.append(card.rank)
    def __str__(self):
        s = "Hand of " + self.name
        if self.is_empty(): # is defined in Deck
            return s + "is empty."
        s += " contains \n" + Deck.__str__(self)
        # uses .__str__() from class Deck which in turn takes from class Card
        return s
    def value(self): # takes member of Hand and its current list of values
        if sum(self.v) > 21: # if a Bust occurs
            j = 0
            while j < len(self.v): # check for an 11
                if self.v[j] == 11: break
                j += 1
            else: # no values in v are equal to 11
                return sum(self.v)
            self.v[j] = 1 # if there are values in v equal to 11, the first 11 is changed
            return self.value() # recursive function; causes the sum of v to be checked again
        else:
            return sum(self.v) # if no Bust occurs, return sum of list v
    def choice(self):
        self.stay = int(input("Stay or Hit? Enter 1 to Stay and 0 to Hit:  "))
        print("\n\n")
        
        #if sum(v) > 21: # if a Bust occurs
         #   for j in range(len(v)):
          #      if v[j] == 11:
           #         v[j] = 1 # change the first 11 to a 1
            #    break
           # return sum(v)
        #else:
         #   return sum(v)
  
class CardGame():
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.Player_1 = input("Enter your Name: ") # asks for name of Player
        self.hand1 = Hand(self.Player_1)
        print("\n")
        self.hand2 = Hand() # The Dealer has the other Hand by default
        self.hands = [self.hand1, self.hand2]
        self.hand1_list = [self.hand1]
        self.hand2_list = [self.hand2]
        #self.deck.deal(self.hands, 2)
        self.bust_bool = False # meaning no one has busted
        self.play = 1 # meaning game in play
    def value_hand1(self): # prints hand1 hand and value
        return self.hand1.__str__() + "\n" + "Value of " + self.hand1.name + "'s Hand: " + str(self.hand1.value())
    def value_hand2(self): # prints hand2 hand and value
        return self.hand2.__str__() + "\n" + "Value of " + self.hand2.name + "'s Hand: " + str(self.hand2.value())
    def __str__(self): #prints both
        return self.value_hand1() + "\n" + "\n" + self.value_hand2() + "\n"
    def end_game(self): # when both Player 1 and Dealer are staying, decide winner
        # deals 2 cards to both to decide winner
        print("Checking whose hand is greater...")
        if self.hand1.value() > self.hand2.value():
            print("You win!")
            self.play = 0
        elif self.hand1.value() < self.hand2.value():
            print("You lose...")
            self.play = 0
        else:
            print("The values of your hands are tied.")
            print("The End Game starts now...")
            print("The Dealer will now deal both of you a card to decide the game.")
            self.hand1 = Hand(self.Player_1) # destroys and makes new Hand for both
            self.hand2 = Hand()
            self.hands = [self.hand1, self.hand2]
            self.deck.deal(self.hands, 2)
            print(self.hand1.name + "'s Card:")
            print(b.hand1.cards[0])
            print("\n")
            print("The Dealer's Card:")
            print(b.hand2.cards[0])
            print("\n")
            if b.hand1.cards[0] > b.hand2.cards[0]: # returns boolean; if Player 1's Card is greater
                print("Your card is greater than the Dealer's.")
                print("You win!")
                self.play = 0
            else:
                print("The Dealer's card is greater than yours.")
                print("You lose...")
                self.play = 0
    def dealer_check(self):
        if self.hand2.value() > 16:
            self.hand2.stay = 1
            print("The Dealer's Hand is locked in! \n")
            print(self)
    def bust(self): # checks if either has busted
        if (self.hand1.value() > 21) and (self.hand2.value() > 21):
            self.bust_bool = True
            print("Both " + self.hand1.name + " and the Dealer have busted!\nYou lose...")
        elif (self.hand1.value() > 21):
            self.bust_bool = True
            print(self.hand1.name + " has busted!\nYou lose...")
        elif (self.hand2.value() > 21):
            self.bust_bool = True
            print("The Dealer has busted!\nYou win!")

b = CardGame() # creates game
# To start,
# The Deck is created,
# The Deck is shuffled,
# Player 1's name is entered
# The Hands of Player 1 and the Dealer are created

while b.play == 1:

    while (int(b.hand1.stay) == 0) and (int(b.hand2.stay) == 0):
        b.deck.deal(b.hands, 2) # A card is dealt to both
        print(b) # Both hands and their values are shown
        b.bust() # checks if anyone has busted
        if b.bust_bool == True:
            b.play = 0
            break
        b.hand1.choice() # Player 1 is given a choice to stay or to hit; will keep or change value of b.hand1.stay
        b.dealer_check() # decides if Dealer will stay or hit; will keep or change value of b.hand2.stay
    
    #if (int(b.hand1.stay) == 0) and (int(b.hand2.stay) == 1): 
    while (int(b.hand1.stay) == 0) and (int(b.hand2.stay) == 1): # Player 1 hasn't stayed yet
        b.deck.deal(b.hand1_list, 1)
        print(b)
        b.bust()
        if b.bust_bool == True:
            b.play = 0
            break
        b.hand1.choice()

    #if (int(b.hand2.stay) == 0) and (int(b.hand1.stay) == 1): # The Dealer hasn't stayed yet
    while (int(b.hand2.stay) == 0) and (int(b.hand1.stay) == 1):
        b.deck.deal(b.hand2_list, 1)
        print(b)
        b.bust()
        if b.bust_bool == True:
            b.play = 0
            break
        b.dealer_check()

    #if (int(b.hand1.stay) == 1) and (int(b.hand2.stay) == 1):
    while (int(b.hand1.stay) == 1) and (int(b.hand2.stay) == 1):
        b.end_game()
        b.play = 0
        break

#b.hit(b.hands) # deals 2 cards so every player gets 1
    #b.hand1 and b.hand2 are objects of Hand
    #b.deck is an object of Deck
#b.hand2.value()
#print(b.hand2.value())

    #print(b.hand2.cards[0].rank) prints rank of card in Hand
