from Deck import Deck, CARD_RANK_FREQUENCIES, MAX_RANK, CARD_RANKS, CARD_SUITS

import logging
import os
#logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger()

NUM_HANDS = 5
HAND_SIZE = 4

class Hand:
    def __init__(self):
        self.cards = []

    def take(self,card):
        self.cards.append(card)

    def give(self,card_index):
        self.cards = self.cards[:card_index] + self.cards[card_index+1:]

    def __repr__(self) -> str:
        rep = "["
        for card in self.cards:
            rep += repr(card) + ", "
        rep += "]"
        return rep

class LostGameError(Exception):
    pass

class WonGameError(Exception):
    pass

class Board:
    def __init__(self):
        self.deck = Deck()
        self.hands = []
        for i in range(NUM_HANDS):
            h = Hand()
            for j in range(HAND_SIZE):
                h.take(self.deck.draw())
            self.hands.append(h)

        self.current_player = 0
        
        self.lives = 3
        self.hints = 8

        self.display = {}
        for suit in CARD_SUITS:
            self.display[suit] = 0

        self.discards = {}
        for suit in CARD_SUITS:
            ranks = {}
            for rank in CARD_RANKS:
                ranks[rank] = 0
            self.discards[suit] = ranks

        self.endgame_timer = None


    def is_indispensible(self,card):
        suit = card.suit
        rank = card.rank
        if self.discards[suit][rank] == (CARD_RANK_FREQUENCIES[rank-1] - 1) :
            return True
        else:
            return False

    
    def is_playable(self,card):
        if self.display[card.suit] == (card.rank - 1):
            return True 
        else:
            return False 
    
    def is_dead(self,card):
        if self.display[card.suit] >= card.rank:
            return True
        else: 
            return False


    def _next_player(self):
        self.current_player += 1
        self.current_player %= NUM_HANDS


    def hint(self):
        log.info("Hint")

        if(self.hints>0):
            self.hints-=1
        else:
            LostGameError()

        self._next_player()


    def discard(self, card_index): 

        hand_index = self.current_player

        hand = self.hands[hand_index]
        card = hand.cards[card_index]

        log.info("Player {} discards {}".format(hand_index,repr(card)))

        # Check loss from discarding indispensible
        if self.is_indispensible(card):
            raise LostGameError()

        # Modify discards
        self.discards[card.suit][card.rank] += 1

        # Modify hints
        self.hints = min(self.hints + 1, 8)

        # Change hand and consider endgame timer
        hand.give(card_index)
        if self.endgame_timer != None:
            if self.endgame_timer == 1:
                raise LostGameError()
            else:
                self.endgame_timer -= 1
        else:
            if self.deck.count_remaining() == 0:
                self.endgame_timer = NUM_HANDS - 1
            else:
                hand.take(self.deck.draw())

        
        self._next_player()


    def play(self, card_index):

        hand_index = self.current_player

        hand = self.hands[hand_index]
        card = hand.cards[card_index]

        log.info("Player {} plays {}".format(hand_index,repr(card)))

        # If play is successful
        if self.is_playable(card):
            log.info("It is successful")

            # Modify display
            self.display[card.suit] += 1

            # Check win
            win_flag = True
            for suit in CARD_SUITS:
                if self.display[suit] != MAX_RANK:
                    win_flag = False 
                    break
            if(win_flag):
                raise WonGameError()

            # Check bonus from completing a suit
            if self.display[card.suit] == MAX_RANK:
                self.hints = min(self.hints + 1, 8)

        # Else play is unsuccessful
        else:
            log.info("It is not successful")

            # Check loss from losing lives
            if self.lives == 1:
                raise LostGameError()
            else:
                self.lives -= 1

            # Check loss from discarding indispensible
            if self.is_indispensible(card):
                raise LostGameError()

            # Modify discards
            self.discards[card.suit][card.rank] += 1

        # Change hand and consider endgame timer
        hand.give(card_index)
        if self.endgame_timer != None:
            if self.endgame_timer == 1:
                raise LostGameError()
            else:
                self.endgame_timer -= 1
        else:
            if self.deck.count_remaining() == 0:
                self.endgame_timer = NUM_HANDS - 1
            else:
                hand.take(self.deck.draw())
        
        self._next_player()


# if __name__ == "__main__":
#     b = Board()
#     b.discard(0)
#     b.discard(0)
#     b.play(0)
#     b.play(0)
#     b.play(0)



