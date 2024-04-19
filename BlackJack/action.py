class Action(object):
    
    """
    This class is essentially just an enumerator for actions
    """
    
    STAND = "STAND"
    HIT = "HIT"
    DOUBLE = "DOUBLE"
    SPLIT = "SPLIT"
    SURRENDER = "SURRENDER"

    @staticmethod
    def all_actions():
        return [Action.STAND, Action.HIT, Action.DOUBLE, Action.SPLIT, Action.SURRENDER]

    # TODO: write info about each action