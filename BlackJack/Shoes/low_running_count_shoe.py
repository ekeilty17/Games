from .shoe import Shoe
import random

class LowRunningCountShoe(Shoe):
    
    """
    This was an attempt to create a malicious shuffling algorithm. The idea is that card counters want high counts, so I will randomly generate shuffles until I get one that does not have too high of a count (up to a certain tolerance).
    
    This turned out to not be very effective due to the cut by one of the players. This cut could potentially convert a low-count shoe into a high-count shoe. The way to get around this is to bound the count on both sides. Meaning we get a shoe where the count is neither very high nor very low. I think this would work in theory, however it's far too slow to effectively test.
    """

    name = "Low Running Count Shoe"

    def __init__(self, count_tolerance=3, *args, **kwargs):
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