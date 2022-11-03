from Deck import Deck, CARD_RANK_FREQUENCIES, MAX_RANK, CARD_RANKS, CARD_SUITS
from Board import Board, Hand, NUM_HANDS, HAND_SIZE, LostGameError, WonGameError

def assign_hand_number(board:Board, hand:Hand):
    # Highest priority of move that can be done with each card 
    for i in range(len(hand.cards)):
        card = hand.cards[i]
        if card.rank==5 and board.is_playable(card):
            return i

    min_rank = 1000
    min_rank_index = -1 
    for i in range(len(hand.cards)):
        card = hand.cards[i]
        if board.is_playable(card) and card.rank<min_rank:
            min_rank = card.rank 
            min_rank_index = i 
    if min_rank_index != -1 :
        return min_rank_index 

    for i in range(len(hand.cards)):
        card = hand.cards[i]
        if board.is_dead(card):
            return i+4
    
    max_rank = -1
    max_rank_index = -1
    for i in range(len(hand.cards)):
        card = hand.cards[i]
        if not board.is_indispensible(card) and card.rank>max_rank:
            max_rank = card.rank 
            max_rank_index = i
    if max_rank_index != -1:
        return max_rank_index+4

    return HAND_SIZE

def recommendation_strategy(board:Board):
    current_player = 0
    recommendations = [HAND_SIZE]*NUM_HANDS
    played_since_hint = 0

    try:
        while True:
            recommendation = recommendations[current_player]
            if recommendation<HAND_SIZE and played_since_hint == 0:
                board.play(recommendation)
            elif recommendation<HAND_SIZE and played_since_hint == 1 and board.lives>1:
                board.play(recommendation)
            elif board.hints>=1:
                board.hint()
                for i in range(NUM_HANDS):
                    if i != current_player:
                        recommendations[i] = assign_hand_number(board,board.hands[i])
            elif recommendation>=HAND_SIZE:
                board.discard(recommendation-HAND_SIZE)
            else:
                board.discard(recommendation-HAND_SIZE)

            current_player+=1
            current_player%=NUM_HANDS
    except LostGameError:
        return 0
    except WonGameError:
        return 1

if __name__ == "__main__":
    cnt = 0
    n = 100000
    for i in range(n):
        b = Board()
        cnt += recommendation_strategy(b)
    print("Wins: {}; Percentage: {}".format(cnt,cnt/n))

    