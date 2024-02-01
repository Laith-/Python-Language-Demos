#AUTHOR LAITH HADDADIN
#SLL taken from lab
import random

class Card:
    
    def __init__(self, rank, suit):
        '''
        Initializes a card object. Cards have a suit and rank. Asserts that the
        provided suit and rank are valid.

        Parameters:
          - rank (string): represents number 2-10, Jack, Queen, King, or Ace
          - suit (string): represents spade, heart, diamond, or club


        Returns: None
        ''' 
        ranks = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
        suits = ['S','H','D','C']
        
        assert isinstance(rank,str),'invalid rank type'
        assert isinstance(suit,str),'invalid suit type'
        assert rank.upper() in ranks,'rank not valid'
        assert suit.upper() in suits,'suit not valid'
        
        self.__suit = suit.upper()
        self.__rank = rank.upper()        
    
        
    def isFaceCard(self):
        face_cards = ['J','Q','K']
        if self.__rank in face_cards:
            return True
        else:
            return False
        
    def isAce(self):
        if self.__rank == 'A':
            return True
        else:
            return False
        
    def isNumeric(self):
        if self.__rank == 'T':
            return True
        else:
            try:
                rank = int(self.__rank)
            except Exception:
                return False
            else:
                return True

    def getRank(self):
        return self.__rank
        
    def getSuit(self):
        return self.__suit
        
    def __str__(self):
        '''
        Informal string representation of the Card object.
        
        Parameters: None
        
        Returns: string
        '''
        return self.__rank + self.__suit
    
class Deck:   
    def __init__(self, capacity):
        assert isinstance(capacity,int),'capacity must be int'
        assert capacity > 0,'capacity has to be greater than zero'
        
        self.__capacity = capacity
        self.__deck = SLL()

    def addCard(self, card):
        self.__deck.add(card,self.__capacity)
        
    def dealCard(self):
        return self.__deck.pop()

    def deckSize(self):
        return self.__deck.getSize()    
    
    def shuffle(self):
        deck = []
        size = self.__deck.getSize()
        while size > 0:
            deck.append(self.__deck.pop())
            size = self.__deck.getSize()
        
        random.shuffle(deck)
        for card in deck:
            self.addCard(card)
        
    def __str__(self):
        return self.__deck.getDeck()
            
class SSLNode:
    def __init__(self,initData,initNext):
        self.data = initData
        self.next = initNext
    def getNext(self):
        return self.next
    def getData(self):
        return self.data
    def setData(self,newData):
        self.data = newData
    def setNext(self,newNext):
        self.next = newNext
        
class SLL:
    def __init__(self):
        self.head = None
        self.size = 0
        
    def add(self,item,capacity):
        # adds an item at the start of the list
        if self.size == capacity:
            raise Exception('deck is full')
        
        new_node = SSLNode(item,None)
        new_node.setNext(self.head)
        self.head = new_node
        self.size = self.size + 1
        
    def append(self,item):
        # adds an item at the end of the list
        new_node = SSLNode(item,None)
        current = self.head # Start the traversal
        if self.size == 0: # check if list is empty
            self.add(item)
        else:
            while (current.getNext()!=None):
                current= current.getNext() # traversing the list
            current.setNext(new_node)
            self.size += 1
 
    def pop(self):
        if self.size == 0:
            raise Exception('deck is empty')
        
        new_head = self.head.getNext()
        old_head = self.head.getData()
        self.head = new_head
        self.size -= 1
        
        return old_head
    
    def getDeck(self):
        # returns a string representation of the list
        current = self.head
        string = []
        while current != None:
            if self.getSize() > 0:
                string.append(str(current.getData()))
                current = current.getNext()
                
        return '-'.join(string)
    
    def getSize(self):
        return self.size    
    
if __name__ == '__main__':
    # test your Card class here
    '''
    
    card = Card('21','c')
    card = Card('2','b')
    
    card = Card('T','c')
    print(card.isFaceCard())
    print(card.isAce())
    print(card.isNumeric())
    print(card.getRank())
    print(card.getSuit())
    print(card)
    '''
    # test your Deck class here
    '''
    
    card1 = Card('2','c')
    card2 = Card('3','h')
    
    deck = Deck(2)
    deck.addCard(card1)
    deck.addCard(card2) #exception is raised if deck capacity is set to 1
    print(deck)
    print(deck.deckSize())
    print(deck.dealCard()) #exception raised if deck empty
    print(deck)
    deck.addCard(card2)
    print(deck)
    deck.shuffle()
    print(deck)
    '''