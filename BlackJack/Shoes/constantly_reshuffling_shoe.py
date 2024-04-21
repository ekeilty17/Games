from .fair_shoe import FairShoe

class ConstantlyReshufflingShoe(FairShoe):

    """
    Card counting becomes most effective at the end of a shoe. A lot of casinos these days implement "Continuous Shuffling Machines" where after each hand cards are redistributed back into the shoe. Thus, rendering card counting completely useless.

    We can model this by simply reshuffling after every hand. This creates a completely unbeatable game.
    """
    
    name = "Constantly Reshuffling Shoe"

    def __init__(self, *args, **kwargs):
        super(ConstantlyReshufflingShoe, self).__init__(ultilized_shoe_percent=0, *args, **kwargs)
        # setting `ultilized_shoe_percent=0` means the CutCard will always be put first, and therefore the code will reshuffle after each hand