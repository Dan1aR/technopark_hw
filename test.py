""" Imports for testting and TicTacToe class """
from unittest import TestCase
from unittest import mock
import unittest

from main import TicTacGame
from text import Text


class TestTicTac(TestCase):
    """ Testing main methods of TicTacToe game """

    def test_validate_move_format(self):
        """ Testting validate function to input has right format """
        game = TicTacGame()
        self.assertTrue(game.validate_move("1")[0])
        self.assertFalse(game.validate_move("qwer")[0])
        self.assertFalse(game.validate_move("0")[0])
        self.assertFalse(game.validate_move("123")[0])

    def test_validate_move_place(self):
        """ Testting validate function if we put move in right place """
        game = TicTacGame()
        mock.builtins.input = lambda _: "1"
        game.move(0)
        self.assertEqual(game.board[0], "X")
        self.assertFalse(game.validate_move("1")[0])

    def test_move(self):
        """ Testting move function as it affecting board """
        game = TicTacGame()

        mock.builtins.input = lambda _: "1"
        game.move(0)
        self.assertEqual(game.board[0], "X")

        mock.builtins.input = lambda _: "2"
        game.move(1)
        self.assertEqual(game.board[1], "O")

    def test_check_winner(self):
        """ Testting check winner function in every possible way"""
        game = TicTacGame()

        game.board = ["X", "X", "X", "O", " ", " ", "O", " ", " "]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.X_WINNER_TEXT)

        game.board = ["O", "O", "O", "X", " ", " ", "X", " ", " "]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.O_WINNER_TEXT)

        game.board = ["X", "O", "O", "X", " ", " ", "X", " ", " "]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.X_WINNER_TEXT)

        game.board = ["O", "X", "X", "O", " ", " ", "O", " ", " "]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.O_WINNER_TEXT)

        game.board = ["X", " ", " ", "O", "X", " ", "O", " ", "X"]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.X_WINNER_TEXT)

        game.board = ["O", " ", " ", "X", "O", " ", "X", " ", "O"]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.O_WINNER_TEXT)

        game.board = [" ", " ", "X", " ", "X", "O", "X", " ", "O"]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.X_WINNER_TEXT)

        game.board = [" ", " ", "O", " ", "O", "X", "O", " ", "X"]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.O_WINNER_TEXT)

        game.board = ["O", "X", "X", "X", "O", "O", "O", "X", "X"]
        is_winner, message = game.check_winner()
        self.assertTrue(is_winner)
        self.assertEqual(message, Text.DRAW_TEXT)

        game.board = [" ", " ", " ", " ", "O", "X", "O", " ", "X"]
        is_winner, message = game.check_winner()
        self.assertFalse(is_winner)


if __name__ == "__main__":
    unittest.main()
