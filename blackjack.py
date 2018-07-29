import random

suits = ['Hearts', 'Spades', 'Diamond', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
		 'Ten', 'King', 'Queen', 'Jack', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
		 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card(object):
	"""docstring for Card"""
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return self.rank + " of " + self.suit

class Deck(object):
	"""docstring for Deck"""
	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit, rank))

	def __str__(self):
		deck_comp = ''
		for card in self.deck:
			deck_comp += '\n' + str(card)
		return "The deck has " + deck_comp	

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		return self.deck.pop()

class Hand(object):
	"""docstring for Hand"""
	def __init__(self):
		self.aces = 0
		self.value = 0
		self.cards = []

	def add_card(self,card):
		self.cards.append(card)
		self.value += values[card.rank]

		if card.rank == 'Ace':
			self.aces += 1

	def adjust_for_aces(self):
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1

class Chips(object):
	"""docstring for Chips"""
	def __init__(self):
		self.total = 100
		self.bet = 0

	def win_bet(self):
		self.total += self.bet	

	def lose_bet(self):
		self.total -= self.bet	


def take_bet(chips):
	while True:
		try:
			chips.bet = int(input("How many chips would you like to bet? "))
		except:
			print("Sorry please provide an integer")
		else:
			if chips.bet > chips.total:
				print("Sorry, you do not have enough chips! You have: {}".format(chips.total))
			else:
				break			

def hit(deck, hand):
	single_card = deck.deal()
	hand.add_card(single_card)
	hand.adjust_for_aces()

def hit_or_stand(deck, hand):
	global playing

	while True:
		x = input("Hit or Stand? Enter h or s ")

		if x.lower() == 'h':
			hit(deck,hand)				
		elif x.lower() == 's':
			print("Player Stands Dealer's Turn")
			playing = False
		else:
			print("Sorry, I did not understand that, Please enter h or s only!")
			continue
		break				

def show_some(player, dealer):
	print("\nDealer Hand!!\nOne hidden")
	print(dealer.cards[1])
	print("\nPlayer Hand!!")
	for card in player.cards:
		print(card)

def show_all(player, dealer):
	print("\nDealer Hand!!")
	for card in dealer.cards:
		print(card)	
	print("\nPlayer Hand!!")
	for card in player.cards:
		print(card)		


def player_busts(player,dealer,chips):
	print("Bust Player!")
	chips.lose_bet()		

def player_wins(player,dealer,chips):
	print("Player Wins!")
	chips.win_bet()

def dealer_busts(player,dealer,chips):
	print("Player Wins! Dealer Busted!")
	chips.win_bet()

def dealer_wins(player,dealer,chips):
	print("Dealer Wins!")
	chips.lose_bet()

def push(player,dealer):
	print("Dealer and Player tie! PUSH")	

# Gameplay

while True:			
	print("WELCOME TO BALCKJACK!! Get as close to 21 as you can without going over!\n\
		Dealer hits until she reaches 17. Aces count as 1 or 11.")

	deck = Deck()
	deck.shuffle()

	player_hand = Hand()
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())

	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())
	# Set up the Player's chips
	player_chips = Chips()
	# Prompt the Player for their bet:
	take_bet(player_chips)

	show_some(player_hand,dealer_hand)

	while playing:
		 # Prompt for Player to Hit or Stand
		hit_or_stand(deck,player_hand)

		show_some(player_hand, dealer_hand)

		if player_hand.value > 21:
			player_busts(player_hand, dealer_hand, player_chips)
			break
	# If Player hasn't busted, play Dealer's hand     
	if player_hand.value <= 21:
		while dealer_hand.value < 17:
			hit(deck,dealer_hand)

		show_all(player_hand, dealer_hand)
		# Test different winning scenarios
		if dealer_hand.value > 21:
			dealer_busts(player_hand, dealer_hand, player_chips)
		elif dealer_hand.value > player_hand.value:
			dealer_wins(player_hand, dealer_hand, player_chips)
		elif dealer_hand.value < player_hand.value:
			player_wins(player_hand, dealer_hand, player_chips)
		else:
			push(player_hand, dealer_hand)

	print("\nPlayer total chips are at: {}".format(player_chips.total))

	new_game = input("Would you like to play another hand? y/n ")

	if new_game[0].lower() == 'y':
		playing = True
		continue
	else:
		break	



					