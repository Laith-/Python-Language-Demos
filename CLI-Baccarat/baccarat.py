#AUTHOR LAITH HADDADIN
from playing_cards import Card, Deck

class Player:
    def __init__(self):
        self.__hand = []
        self.__handValue = 0
    
    def updateHand(self, card):
        self.__hand.append(card)
        value = 0
        if card.isNumeric():
            if card.getRank() == 'T':
                value = 0
            else:
                value = int(card.getRank())
        elif card.isAce():
            value = 1
        elif card.isFaceCard():
            value = 0
        
        self.__handValue += value
        self.__handValue = self.__handValue%10
        
    def clearHand(self):
        self.__hand = []
        self.__handValue = 0
    
    def getHand(self):
        return self.__hand
    
    def getHandValue(self):
        return self.__handValue
              

class Table:
    DISCARD = [] #discarded cards
    
    def __init__(self):
        self.__deck = Deck(52)
        self.__player = Player()
        self.__dealer = Player()
    
    def populateDeck(self):
        file_dir = input('Enter the input filename: ')
        file = open(file_dir, 'r').read().strip().split()
        if len(file) != 52:
            raise Exception('wrong amount of cards in file')

        unique_cards = []
        
        for prop in file:
            if prop in unique_cards:
                raise Exception('duplicate card')
            
            unique_cards.append(prop)
            card_prop = list(prop)
            card = Card(card_prop[0],card_prop[1])
            self.__deck.addCard(card)

            
    def cardsRemaining(self):
        return self.__deck.deckSize()
    
    def deal(self, toWho):
        turn = toWho%2
        card = self.__deck.dealCard()
        if turn == 0:
            #player
            self.__player.updateHand(card)
        elif turn == 1:
            #dealer
            self.__dealer.updateHand(card)
        
        return card
    
    def displayTable(self):
        player_cards_list = []
        dealer_cards_list = []
        
        for card in self.__player.getHand():
            player_cards_list.append(str(card))
        player_cards = ' '.join(player_cards_list)
        
        for card in self.__dealer.getHand():
            dealer_cards_list.append(str(card))        
        dealer_cards = ' '.join(dealer_cards_list)
        
        print('Player :', player_cards, '--> Score =', self.__player.getHandValue())
        print('Player :', dealer_cards, '--> Score =', self.__dealer.getHandValue())
    
    def checkTableValues(self):
        return (self.__player.getHandValue(),self.__dealer.getHandValue())
    
    def clearTable(self):
        #clear player hand
        for cards in self.__player.getHand():
            self.DISCARD.append(cards)
        self.__player.clearHand()
        
        #clear dealer hand
        for cards in self.__dealer.getHand():
            self.DISCARD.append(cards)
        self.__dealer.clearHand()
        
    def newDeck(self):
        for card in range(len(self.DISCARD)):
            self.__deck.addCard(self.DISCARD.pop())
        self.__deck.shuffle()
      
def main():
    print('*******************')
    print('Welcome to BACCARAT')
    print('*******************')
    
    turn = 0
    round_number = 1
    play_again = True
    
    game =  Table()
    game.populateDeck()    
    
    while play_again:
        print('\nROUND',round_number)
        print('----------')     

        while turn < 2:
            game.deal(turn)
            turn += 1
            game.deal(turn)
            
        game.displayTable()
        outcome = deal_cards(game,round_number)
        play_again = keep_playing()
        
        if play_again:
            turn = 0
            round_number += 1
            game.clearTable()
            check_deck(game)
    
def deal_cards(game,round_number):
    hands = game.checkTableValues()
    player_hand = hands[0]
    dealer_hand = hands[1]
    
    natural = False
    
    for i in hands:
        if i in range(8,10):
            natural = True
    if natural:
        message = ''
        who_won = ''
        
        who_won = 'PLAYER'
        message = 'NATURAL! {} wins round {}!'.format(who_won,round_number)
        if dealer_hand > player_hand:
            who_won = 'DEALER'
            message = 'NATURAL! {} wins round {}!'.format(who_won,round_number)
        elif dealer_hand == player_hand:
            who_won = 'TIE'
            message = 'NATURAL! Round {} is a tie!'.format(round_number)
        
        print(message)    

    else:
        player_dealt = False
        dealer_dealt = False
        
        if player_hand not in range(6,8) and player_hand in range(0,6):
            player_card = game.deal(0)
            player_dealt = True
            print('Player draws',player_card)
        else:
            print('Player stands')
            
        if not player_dealt and dealer_hand not in range(6,8) and dealer_hand in range(0,6):
            dealer_card = game.deal(1)
            dealer_dealt = True
            print('Dealer draws',dealer_card)
        else:
            #dealer conditions for getting a card
            if dealer_hand <= 2:
                dealer_card = game.deal(1)
                dealer_dealt = True
                print('Dealer draws',dealer_card) 
                
            elif player_dealt and dealer_hand == 3:
                if player_card.isNumeric():
                    if int(player_card.getRank()) == 8:
                        dealer_card = game.deal(1)
                        dealer_dealt = True
                        print('Dealer draws',dealer_card)
            
            elif player_dealt and dealer_hand == 4:
                if player_card.isNumeric():
                    if int(player_card.getRank()) in range(2,8):
                        dealer_card = game.deal(1)
                        dealer_dealt = True
                        print('Dealer draws',dealer_card)
            
            elif player_dealt and dealer_hand == 5:
                if player_card.isNumeric():
                    if int(player_card.getRank()) in range(4,8):
                        dealer_card = game.deal(1)
                        dealer_dealt = True
                        print('Dealer draws',dealer_card)
                        
            elif player_dealt and dealer_hand == 6:
                if player_card.isNumeric():
                    if int(player_card.getRank()) in range(6,8):                        
                        dealer_card = game.deal(1)
                        dealer_dealt = True
                        print('Dealer draws',dealer_card)
                                                 
            else:
                print('Dealer stands')
        
        game.displayTable()
        is_winner(game,round_number)
        
        
def is_winner(game,round_number):
    hands = game.checkTableValues()
    player_hand = hands[0]
    dealer_hand = hands[1]    
    
    who_won = 'PLAYER'
    message = '{} wins round {}!'.format(who_won,round_number)
    if dealer_hand > player_hand:
        who_won = 'DEALER'
        message = '{} wins round {}!'.format(who_won,round_number)
    elif dealer_hand == player_hand:
        who_won = 'TIE'
        message = 'Round {} is a tie!'.format(round_number)
    
    print(message)

def keep_playing():
    play = input('**********\nPlay another round? (Y/N) ')
    play_again = True
    if play.upper() == 'N':
        play_again = False
        print('Thanks for playing...Goodbye.')
    
    return play_again

def check_deck(game): 
    if game.cardsRemaining() < 6:
        print('Not enough cards for another round.  Creating a new deck.')
        game.newDeck()
            
if __name__=='__main__':
    # main baccarat game should be run from here
    main()