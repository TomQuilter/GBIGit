class GridWorldGame:
    def __init__(self):
        # Initialize the 5x5 game board
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        # Set the starting positions of the players
        self.board[0][0] = 'X'
        self.board[4][4] = 'O'
        # Set the positions of the barriers
        for i in [0, 1, 3, 4]:  # Set barriers at C1, C2, C4, C5
            self.board[i][2] = '#'
        # Set the current player to 'X'
        self.current_player = 'X'
        # Define the winning rows for each player
        self.winning_rows = {'X': 4, 'O': 0}

    def print_board(self):
        print("  A B C D E")
        for i in range(5):
            print(f"{5 - i}", end=" ")
            for j in range(5):
                print(self.board[i][j], end=" ")
            print()

    def is_winner(self, player):
        for i in range(5):
            if self.board[self.winning_rows[player]][i] == player:
                return True
        return False

    def get_moves(self, row, col):
        moves = []
        opponent = 'O' if self.current_player == 'X' else 'X'
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < 5 and 0 <= new_col < 5 and self.board[new_row][new_col] == ' ':
                    # Block forward diagonal moves when blocked by the opponent
                    if self.current_player == 'X' and new_row > row and self.board[row][new_col] == opponent:
                        continue
                    if self.current_player == 'O' and new_row < row and self.board[row][new_col] == opponent:
                        continue
                    moves.append((new_row, new_col))
        return moves

    def play(self):
        while True:
            self.print_board()
            print(f"{self.current_player}'s turn")
            row, col = None, None
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == self.current_player:
                        row, col = i, j
                        break
            moves = self.get_moves(row, col)
            if not moves:
                print(f"{self.current_player} has no valid moves. The game is a draw!")
                break
            move_str = input("Enter your move (e.g. B3): ").upper()
            col_str, row_str = move_str[0], move_str[1]
            move_col = ord(col_str) - ord('A')
            move_row = 5 - int(row_str)
            if (move_row, move_col) not in moves:
                print("Invalid move! Please enter a valid move.")
                continue
            self.board[row][col] = ' '
            self.board[move_row][move_col] = self.current_player
            if self.is_winner(self.current_player):
                self.print_board()
                print(f"{self.current_player} wins!")
                break
            self.current_player = 'O' if self.current_player == 'X' else 'X'


if __name__ == "__main__":
    game = GridWorldGame()
    game.play()
