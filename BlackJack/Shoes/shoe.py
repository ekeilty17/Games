from card import Card, CutCard
import random

class Shoe(object):

    all_pips = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    all_suits = ['H', 'C', 'D', 'S']

    def __init__(self, number_of_decks=4, ultilized_shoe_percent=0.8, seed=None):
        self._number_of_decks = number_of_decks
        self._ultilized_percent = ultilized_shoe_percent    # BlackJack apprentice calls this `penentration`
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
        end_of_shoe_index = int( self._ultilized_percent * len(self.cards) ) + 1
        self.cards.insert(end_of_shoe_index, self.cut_card)

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
        # self._check_shuffle()
        self._c = 0

    # Some of the other shuffling functions get complicated. This function makes sure they maintained the deck
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

    
    def _get_running_count(self):
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


if __name__ == "__main__":

    D = Shoe(number_of_decks=4)
    D.shuffle()
    D.cut()
    D.place_cut_card()
    print(D)