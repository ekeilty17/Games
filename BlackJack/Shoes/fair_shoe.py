from .shoe import Shoe
import random

class FairShoe(Shoe):

    name = "Fair Shoe"

    def shuffle_cards(self):
        random.shuffle(self.cards)