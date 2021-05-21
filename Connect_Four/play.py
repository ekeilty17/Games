from grid import ConnectFourGrid
import os

def human_player(C):

    valid = False
    while not valid:
        c = input("\tChoose a column: ")
        try:
            if int(float(c)) != float(c) or int(c) < 1 or int(c) > C.w:
                print("\tinvalid input")
            else:
                valid = True
        except:
            print("\tinvalid input")
    return int(c)

def play_connect_four(player1, player2):

    C = ConnectFourGrid()
    os.system('clear')
    print(C)

    while True:

        print("\nPlayer 1's Turn:")
        p1_move = player1(C)
        C.move(player=1, c=p1_move)
        os.system('clear')
        print(C)

        if C.check_win():
            break
        
        if C.is_full():
            break

        print("\nPlayer 2's Turn:")
        p2_move = player2(C)
        C.move(player=2, c=p2_move)
        os.system('clear')
        print(C)

        if C.check_win():
            break
        
        if C.is_full():
            break

    winning_player = C.check_win()
    if winning_player == 0:
        print("It's a Tie")
    else:
        print(f"Player {winning_player} wins!")

if __name__ == "__main__":
    play_connect_four(human_player, human_player)