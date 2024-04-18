from card import Card, CutCard
import random
import math

class Shoe(object):

    all_pips = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    all_suits = ['H', 'C', 'D', 'S']

    def __init__(self, number_of_decks=4, ultilized_shoe_percent=0.8, seed=None):
        self._number_of_decks = number_of_decks
        self._ultilized_percent = ultilized_shoe_percent
        self.cut_card = CutCard()
        
        self.seed = seed
        if not self.seed is None:
            random.seed(self.seed)

        self.cards = []
        self.reset_deck()

        # left of `self.c` are the cards that have already been dealt
        # right of the `self.c` are the cards that have yet to be dealt
        self._c = 0

    def __repr__(self):
        str_cards = [str(card) for card in self.cards]
        return ' '.join(str_cards)

    def __len__(self):
        return len(self.cards)
    
    def __iter__(self):
        return self.cards.__iter__()

    def set_number_of_decks(self, number_of_decks):
        self._number_of_decks = number_of_decks
        self.reset_deck()

    def reset_deck(self):
        self.cards = []
        for i in range(self._number_of_decks):
            self.cards.extend( self._new_deck() )

    # provides a list of cards in new deck order
    def _new_deck(self):
        new_deck = []
        for suit in self.all_suits:
            ordered_pips = list(self.all_pips)
            if suit in ['D', 'S']:
                ordered_pips = reversed(ordered_pips)
            new_deck.extend( [Card(pip, suit) for pip in ordered_pips] )
        return new_deck

    def place_cut_card(self):
        end_of_shoe_index = int( self._ultilized_percent * len(self.cards) )
        self.cards.insert(end_of_shoe_index, self.cut_card)

    def burn_card(self):
        self._c += 1

    def deal(self):
        if self._c == len(self.cards):
            raise IndexError("All cards in the deck have been dealt. Please reshuffle.")

        card = self.cards[self._c]
        self._c += 1
        return card

    # This is a custom shuffle function implemented in child classes
    def shuffle_cards(self):
        raise NotImplementedError("Not yet implemented...")
        # Does not need to return anything. Should just modify `self.cards`

    # This is what is called by the user
    def shuffle(self):
        if self.cut_card in self.cards:
            self.cards.remove(self.cut_card)
        self.shuffle_cards()
        self._check_shuffle()
        self._c = 0

    def _check_shuffle(self):
        cards_copy = list(sorted( list(self.cards), key=lambda c: str(c) ))
        
        new_deck = []
        for i in range(self._number_of_decks):
            new_deck.extend( self._new_deck() )
        new_deck = list(sorted( new_deck, key=lambda c: str(c) ))

        if len(cards_copy) != len(new_deck):
            raise ValueError(f"The shuffle modified the number of cards in the shoe. Got {len(cards_copy)} but expected {len(new_deck)}")

        for c1, c2 in zip(cards_copy, new_deck):
            if str(c1) != str(c2):
                raise ValueError(f"The shuffle either added or removed a card from the shoe.")

    def cut(self, cut_index=None):
        if cut_index is None:
            cut_index = random.randint(0, len(self.cards))
        cut_index %= len(self.cards)
        self.cards =  self.cards[cut_index:] + self.cards[:cut_index]

    def get_running_count(self):
        running_count = 0
        history = [0]
        for card in self.cards:
            if card == CutCard():
                continue
            if 2 <= card.value <= 6:
                running_count -= 1
            elif card.value == 1 or card.value== 10:
                running_count += 1
            history.append(running_count)
        return history


class FairShoe(Shoe):

    def shuffle_cards(self):
        random.shuffle(self.cards)



class LowRunningCountShoe(Shoe):
    
    """
    This is my low fidelity model of auto-shufflers which produce a completely new shoe, but is still hand dealt
    Since it's out of the auto-shuffler it can no longer influence the cards, however, they can try their best to evenly distribute the cards to prevent card counters from getting a high count

    This is made harder if we allow the players to cut the cards as the alg can't precisely calculate the count
    """

    def __init__(self, count_tolerance=4, *args, **kwargs):
        super(LowRunningCountShoe, self).__init__(*args, **kwargs)
        self.count_tolerance = count_tolerance

    def _is_count_too_high(self):
        running_count = 0
        # count_too_high = False
        for i, card in enumerate(self.cards):
            if 2 <= card.value <= 6:
                running_count -= 1
            elif card.value == 1 or card.value== 10:
                running_count += 1
            
            # True count actually isn't as good of a metric because the player can cut the cards and change everything
            # num_decks_remaining = (52*self._number_of_decks - i - 1) / (52*self._number_of_decks)
            # true_count = running_count / num_decks_remaining
            # print((52*self._number_of_decks - i - 1), num_decks_remaining, running_count, true_count)

            # print((52*self._number_of_decks - i - 1), running_count)
            if (running_count <= -self.count_tolerance) or (running_count >= self.count_tolerance):
                # count_too_high = True
                return True
        # return count_too_high
        return False

    def shuffle_cards(self):
        random.shuffle(self.cards)
        while self._is_count_too_high():
            random.shuffle(self.cards)
    

class ConstantlyReshufflingShoe(FairShoe):

    """
    By putting the cut card at the beginning of the shoe, my blackjack program is going to reshuffle every hand
    This is my low fidelity model of the continuous auto-shufflers since cards get put back into them they are being continuously reshuffled back into the deck
    """
    
    def __init__(self, *args, **kwargs):
        super(ConstantlyReshufflingShoe, self).__init__(ultilized_shoe_percent=0, *args, **kwargs)


class EvenlyDistributedHighCards(FairShoe):
    
    def __init__(self, high_cards_per_bucket=2, *args, **kwargs):
        super(EvenlyDistributedHighCards, self).__init__(*args, **kwargs)
        self.high_cards_per_bucket = high_cards_per_bucket

    @staticmethod
    def flatten_to_2d_list(L, sublist_length):
        return [L[i:i+sublist_length] for i in range(0, len(L), sublist_length)]

    def shuffle_cards(self):
        # separate high and low cards
        high_cards = []
        low_cards = []
        for card in self.cards:
            if card.value == 10 or card.value == 1:
                high_cards.append(card)
            else:
                low_cards.append(card)
        
        # shuffle both
        random.shuffle(high_cards)
        random.shuffle(low_cards)
        
        # now we create buckets
        H = self.flatten_to_2d_list(high_cards, self.high_cards_per_bucket)
        low_cards_per_bucket = len(low_cards) // len(H)
        L = self.flatten_to_2d_list(low_cards, low_cards_per_bucket)

        # merge them
        merged_cards = []
        for h, l in zip(H, L):
            bucket = h + l
            random.shuffle(bucket)      # we shuffle the bucket so the 10 is always in the same place
            merged_cards.extend(bucket)
        
        # if len(H) doesn't evenly divide len(low_cards) we could have an extra bucket that wasn't matched
        if len(H) < len(L):
            for i in range(len(H), len(L)):
                merged_cards.extend(L[i])

        self.cards = merged_cards


if __name__ == "__main__":

    #D = FairShoe(number_of_decks=2)
    #D = LowRunningCountShoe(number_of_decks=2)
    #D = ConstantlyReshufflingShoe(number_of_decks=2)
    D = EvenlyDistributedHighCards(number_of_decks=4)
    D.shuffle()
    D.cut()
    D.place_cut_card()
    print(D)
    print()
    history = D.get_running_count()
    print(history)
    print(max(history))
    print(min(history))