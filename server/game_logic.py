

def check_winner(board, player):
    """
    Kontrollon nëse lojtari ka fituar.
    """
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], 
        [0, 3, 6], [1, 4, 7], [2, 5, 8], 
        [0, 4, 8], [2, 4, 6]             
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False


def is_board_full(board):
    """
    Kontrollon nëse tabela është e plotë (barazim).
    """
    return ' ' not in board