from AI import *

#Testing
Unique_Candidate_Test = [
    [0, 0, 4,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],

    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 4, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],

    [5, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 4,    0, 0, 0]   ]

Soul_Candidate_Test = [
    [0, 0, 0,    0, 0, 1,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 6,    0, 0, 0],

    [0, 0, 0,    4, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 8, 0,    0, 0, 0],
    [2, 0, 9,    0, 0, 0,    0, 0, 7],

    [0, 0, 0,    0, 0, 0,    0, 0, 0],
    [0, 0, 0,    0, 0, 3,    0, 0, 0],
    [0, 0, 0,    0, 0, 0,    0, 0, 0]   ]

getCandidates_Test = [
    [0, 0, 0,    0, 0, 0,    0, 0, 2],
    [0, 0, 0,    0, 9, 5,    4, 0, 0],
    [0, 0, 6,    8, 0, 0,    0, 0, 0],

    [0, 8, 5,    0, 2, 0,    9, 4, 1],
    [0, 0, 0,    1, 0, 9,    7, 3, 8],
    [1, 0, 0,    0, 0, 0,    2, 5, 6],

    [8, 9, 3,    0, 1, 0,    0, 0, 0],
    [0, 0, 0,    9, 0, 0,    0, 0, 4],
    [0, 0, 7,    6, 0, 0,    3, 0, 0]   ]

def AI_Testing(game_board):
    B = board(game_board)
    B.Display()
    
    #Unique_Candidate(B)
    #Soul_Candidate(B, [5,5])
    for j in range(9):
        print getCandidates(B.store,[0,j])
    #B.Display()

#AI_Testing(Unique_Candidate_Test)
#AI_Testing(Soul_Candidate_Test)
AI_Testing(getCandidates_Test)
