
import unittest
from server.game_logic import check_winner, is_board_full

class TestGameLogic(unittest.TestCase):
    def test_check_winner(self):
        board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertTrue(check_winner(board, 'X'))

    def test_is_board_full(self):
        board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
        self.assertTrue(is_board_full(board))

if __name__ == "__main__":
    unittest.main()