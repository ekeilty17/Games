from .shoe import Shoe
import random

class EvenlyDistributedHighCardsShoe(Shoe):
    
    """
    Card counters gain an advantage when high cards are clumped together (especially at the end of a shoe), causing a high count. To prevent this situation, this malicious algorithm forces high cards to be evenly distributed throughout the shoe.

    This is done by creating regular buckets. While high-cards can be anywhere within these buckets, we are ensuring only a fixed number appear in each. Thus, the count can never get too high.

    We could improve on this algorithm in a number of ways. For example, separating high, medium, and low. We could also make the buckets different sizes so that players couldn't exploit the regularity of the high-cards. Maybe this is something I will experiment with in the future.
    """

    name = "Evenly Distributed High Cards Shoe"

    def __init__(self, high_cards_per_bucket=2, *args, **kwargs):
        super(EvenlyDistributedHighCardsShoe, self).__init__(*args, **kwargs)
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