""" Text collections """
from text import Text


class TicTacGame:
    """TicTacToe gameplay implementation"""

    def __init__(self) -> None:
        self.board = [" " for _ in range(9)]

    def show_board(self):
        """Harcoded prints to show self.board"""
        print("\n")
        print("\t     |     |")
        print(f"\t  {self.board[0]}  |  {self.board[1]}  |  {self.board[2]}")
        print("\t_____|_____|_____")

        print("\t     |     |")
        print(f"\t  {self.board[3]}  |  {self.board[4]}  |  {self.board[5]}")
        print("\t_____|_____|_____")

        print("\t     |     |")
        print(f"\t  {self.board[6]}  |  {self.board[7]}  |  {self.board[8]}")
        print("\t     |     |")
        print("\n")

    def move(self, move_count):
        """Read Users input validating it and move"""
        move = input(">> ")
        is_valid, message = self.validate_move(move)
        while not is_valid:
            print(message)
            move = input(">> ")
            is_valid, message = self.validate_move(move)

        move = int(move)
        move_char = "X" if move_count % 2 == 0 else "O"
        self.board[move - 1] = move_char

    def validate_move(self, move):
        """Validating string to convert to move"""
        try:
            move = int(move)
            if move not in range(1, 10):
                return False, Text.NOT_IN_MODE_RANGE_TEXT

            if self.board[move - 1] != " ":
                return False, Text.WRONG_PLACE_TEXT

            return move, ""
        except ValueError:
            return False, Text.NOT_INT_INPUT_TEXT

    def start_game(self):
        """Main for this class"""
        move_count = 0
        is_winner, message = self.check_winner()
        while not is_winner:
            print(message)
            if move_count % 2 == 0:
                print(Text.X_MOVE_TEXT)
                self.move(move_count)
            else:
                print(Text.O_MOVE_TEXT)
                self.move(move_count)

            self.show_board()
            move_count += 1

            is_winner, message = self.check_winner()
	    
        print(message)

    def check_winner(self):
        """Method checks rows, columns and diagonales to find out if there is a winner on board"""

        rows = {"".join(self.board[3 * i : 3 * i + 3]) for i in range(3)}
        columns = {
            "".join([self.board[i], self.board[i + 3], self.board[i + 6]])
            for i in range(3)
        }
        diagonals = set(
            [
                "".join([self.board[0], self.board[4], self.board[8]]),
                "".join([self.board[6], self.board[4], self.board[2]]),
            ]
        )

        if "XXX" in rows | columns | diagonals:
            return True, Text.X_WINNER_TEXT

        if "OOO" in rows | columns | diagonals:
            return True, Text.O_WINNER_TEXT

        if " " not in self.board:
            return True, Text.DRAW_TEXT

        return False, ""


if __name__ == "__main__":
    print(Text.HELLO_TEXT)

    game = TicTacGame()
    game.start_game()
