"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0
    empty = 0
    for row in board:
        for item in row:
            if item == EMPTY:
                empty += 1 
            elif item == X:
                x += 1
            else:
                o += 1
    
    if x>o:
        return O
    else:
        return X  


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if action is available
    if not action in actions(board):
        raise NameError('Action is not available!')

    # Copy the board using the deepcopy function
    copy_board = copy.deepcopy(board)
    # The action is a tulpe with the index of the row and colum 
    copy_board[action[0]][action[1]] = player(copy_board)

    # Return the new bord with the action
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check i 3 horizontal value are equal but not EMPTY
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
    
    # Check i 3 vertical value are equal but not EMPTY
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    
    # Check diagonal value, else returne None
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Return True IF(there is a winner or there is no EMPTY space in the board), ELSE return false
    if winner(board) != None:
        return True
    elif not EMPTY in board[0] and not EMPTY in board[1] and not EMPTY in board[2]:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check the max value for a specific board
    def maxValue(newBoard):
        v = -math.inf
        
        # If the game is over return the result
        if terminal(newBoard):
            return utility(newBoard)
        
        for action in actions(newBoard):
            v = max(v,minValue(result(newBoard, action)))
        return v
        
    # Check the min value for a specific board
    def minValue(newBoard):
        v = math.inf

        # If the game is over return the result
        if terminal(newBoard):
            return utility(newBoard)
        
        for action in actions(newBoard):
            v = min(v,maxValue(result(newBoard, action)))
        return v
        
    if player(board) == X:
        best_score = -math.inf
        for action in actions(board):
            score = minValue(result(board,action))
            if score > best_score:
                best_score = score
                best_action = action
                if best_score == 1:
                    return action
    else: 
        best_score = math.inf
        for action in actions(board):
            score = maxValue(result(board,action))
            if score < best_score:
                best_score = score
                best_action = action
                if best_score == -1:
                    return action

    return best_action

            
