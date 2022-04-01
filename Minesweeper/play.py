import argparse
from engine import MinesweeperEngine

def get_args():
    # Command Line Arguments
    parser = argparse.ArgumentParser(description='Terminal Arguments for Minesweeper')
    
    # for preset difficulties
    parser.add_argument('--beginner', action="store_true", default=False)
    parser.add_argument('--intermediate', action="store_true", default=False)
    parser.add_argument('--expert', action="store_true", default=False)
    
    # custom parameters
    parser.add_argument('--custom', action="store_true", default=False)
    parser.add_argument('-H', type=int, default=16, help="height of custom grid")
    parser.add_argument('-W', type=int, default=16, help="width of custom grid")
    parser.add_argument('-M', type=int, default=40, help="number of mines in custom grid")
    
    args = parser.parse_args()
    return args

def main(args):
    
    beginner = {"height": 9, "width": 9, "number_of_mines": 10}
    intermediate = {"height": 16, "width": 16, "number_of_mines": 40}
    expert = {"height": 16, "width": 30, "number_of_mines": 99}

    game_params = {}
    if args.beginner:
        game_params = beginner
    elif args.intermediate:
        game_params = intermediate
    elif args.expert:
        game_params = expert
    elif args.custom:
        game_params = {"height": args.H, "width": args.W, "number_of_mines": args.M}
    else:
        # beginner is the default game
        game_params = beginner
    
    engine = MinesweeperEngine(verbose=False, **game_params)
    engine.run()

if __name__ == "__main__":
    args = get_args()
    main(args)