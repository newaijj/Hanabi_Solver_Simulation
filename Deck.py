
import random


CARD_RANKS = [1,2,3,4,5]
MAX_RANK = len(CARD_RANKS)
CARD_RANK_FREQUENCIES = [3,2,2,2,1]
CARD_SUITS = ["R","Y","G","B","W"]

class Card:
    def __init__(self,rank,suit):
        self.rank = rank 
        self.suit = suit 

    def __repr__(self):
        return self.suit + "_" + str(self.rank)

class Deck:
    def __init__(self):
        cards = []
        for suit in CARD_SUITS:
            for rank,freq in zip(CARD_RANKS,CARD_RANK_FREQUENCIES):
                for i in range(freq):
                    cards.append(Card(rank,suit))
        random.shuffle(cards)
        self.cards = cards

    def __repr__(self) -> str:
        return "Deck of {} cards".format(len(self.cards))

    def draw(self):
        assert(len(self.cards)>0)
        fst = self.cards[0]
        self.cards = self.cards[1:]
        return fst 

    def count_remaining(self):
        return len(self.cards)



if __name__ == "__main__":
    d = Deck()
    print(d.draw())
    print(d.draw())
    print(d.draw())

