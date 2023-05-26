from tictactoe import initial_state, player, actions, result, winner, terminal, utility


X = "X"
O = "O"
EMPTY = None

board = [[X, O, O],
        [O, X, O],
        [X, O, O]]

#print(player(board))
#print(actions(board))
#print(result(board, (0,0)))
print(winner(board))
#print(terminal(board))
#print(utility(board))