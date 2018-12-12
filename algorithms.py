import copy
import random
import math
    
def cozmoDecentMove(board, cozmo, human):
    best = -1000
    moveRow, moveCol = -1, -1

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == " ":
                board[row][col] = cozmo
                value = minimax(0, False, board, cozmo, human)
                board[row][col] = " "
                if value > best:
                    moveRow = row
                    moveCol = col
    return moveRow, moveCol

def cozmoRandomMove(board):
    row, col = random.randint(0, 2), random.randint(0, 2)
    while board[row][col] != " ":
        row, col = random.randint(0, 2), random.randint(0, 2)
    return row, col

def testWinMove(board, piece, row, col):
    bCopy = copy.deepcopy(board)
    bCopy[row][col] = piece
    if piece == "X":
        other = "O"
    else:
        other = "X"
    return evaluateVictory(bCopy, piece, other) != 0

def testForkMove(board, piece, row, col):
    # Determines if a move opens up a fork
    bCopy = copy.deepcopy(board)
    bCopy[row][col] = piece
    winningMoves = 0
    for row in range(0, 3):
        for col in range(0, 3):
            if testWinMove(bCopy, piece, row, col) and bCopy[row][col] == ' ':
                winningMoves += 1
    return winningMoves >= 2

def cozmoBestMove(board, cozmo, human):
    # Check computer win moves
    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == ' ' and testWinMove(board, cozmo,row, col):
                return row, col
    # Check player win moves
    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == ' ' and testWinMove(board, human, row, col):
                return row, col
    # Check computer fork opportunities
    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == ' ' and testForkMove(board, cozmo, row, col):
                return row, col
    # Check player fork opportunities, incl. two forks
    playerForks = 0
    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == ' ' and testForkMove(board, human, row, col):
                playerForks += 1
                tempRow, tempCol = row, col
    if playerForks == 1:
        return tempRow, tempCol
    elif playerForks == 2:
        if board[0][1] == ' ':
            return 0, 1
        if board[1][0] == " ":
            return 1, 0
        if board[1][2] == " ":
            return 1, 2
        if board[2][1] == " ":
            return 2, 1
    # Play center
    if board[1][1] == ' ':
        return 1, 1
    # Play a corner
    if board[0][0] == ' ':
        return 0, 0
    if board[0][2] == " ":
        return 0, 2
    if board[2][0] == " ":
        return 2, 0
    if board[2][2] == " ":
        return 2, 2
    #Play a side
    if board[0][1] == ' ':
        return 0, 1
    if board[1][0] == " ":
        return 1, 0
    if board[1][2] == " ":
        return 1, 2
    if board[2][1] == " ":
        return 2, 1

# minimax game algorithm description: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/

def movesLeft(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == " ":
                return True
    return False

def evaluateVictory(board, cozmo, human):
    #checking rows
    for row in range(len(board)):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == cozmo:
                return 10
            elif board[row][0] == human:
                return -10
    
    #checking columns
    for col in range(len(board)):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == cozmo:
                return 10
            elif board[0][col] == human:
                return -10
    
    #checking diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            if board[0][0] == cozmo:
                return 10
            elif board[0][0] == human:
                return -10
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            if board[0][2] == cozmo:
                return 10
            elif board[0][2] == human:
                return -10
    return 0

def minimax(depth, isMax, board, cozmo, human):
    score = evaluateVictory(board, cozmo, human)
    #cozmo win
    if score == 10:
        return score 
    #human win
    if score == -10:
        return score
    #tie
    if not movesLeft(board):
        return 0

    #maximizer's move 
    if isMax:
        best = -1000
        #Traverse all cells 
        for row in range(len(board)):
            for col in range(len(board[row])):
                #check if empty 
                if board[row][col] == " ": 
                    #make the move 
                    board[row][col] = cozmo
                    best = max(best, minimax(depth+1, not isMax, board, cozmo, human))
                    #undo
                    board[row][col] = " "
        return best
    else:
        best = 1000
        #Traverse all cells 
        for row in range(len(board)):
            for col in range(len(board[row])):
                #check if empty 
                if board[row][col] == " ": 
                    #make the move 
                    board[row][col] = human
                    best = min(best, minimax(depth+1, not isMax, board, cozmo, human));
                    #undo
                    board[row][col] = " "; 

        return best