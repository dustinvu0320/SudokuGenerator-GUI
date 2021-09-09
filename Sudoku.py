from random import shuffle
import copy


# Solve sudoku game using backtracking
def solve(board):
    find = is_empty(board)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if is_valid(board, row, col, i):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


# Check number is valid at that position
def is_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


# Check number is valid at that position
def is_valid(board, row, col, num):
    # Check row
    for i in range(9):
        if board[row][i] == num and col != i:
            return False
    # Check column
    for i in range(9):
        if board[i][col] == num and row != i:
            return False
    # Check box
    x = row // 3
    y = col // 3
    for i in range(x * 3, x * 3 + 3):
        for j in range(y * 3, y * 3 + 3):
            if board[i][j] == num and (i, j) != (row, col):
                return False

    return True


class SudokuGenerator:
    # Initialize board
    def __init__(self):
        self.counter = 0
        self.board = [[0 for i in range(9)] for j in range(9)]
        # Generate a sudoku board
        self.create_board(self.board)
        # Deepcopy (keep the original fully board)
        self.original_board = copy.deepcopy(self.board)
        # self.print_board()
        self.remove_numbers_from_board()
        # self.print_board()

    # Print sudoku board
    def print_board(self):
        temp = self.board
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                # The end of the row, go to next line
                if j == 8:
                    print(temp[i][j])
                else:
                    print(str(temp[i][j]) + " ", end="")
        print("")

        # Function solve the sudoku using backtracking
    def solve_puzzle(self, board):
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            # Find next empty spot
            if board[row][col] == 0:
                for number in range(1, 10):
                    # Check if spot is valid
                    if is_valid(board, row, col, number):
                        board[row][col] = number
                        if not is_empty(board):
                            self.counter += 1
                            break
                        else:
                            if self.solve_puzzle(board):
                                return True
                break
        board[row][col] = 0
        return False

    # Generate a fully sudoku board
    def create_board(self, board):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            # Find next empty spot
            if board[row][col] == 0:
                shuffle(number_list)
                for number in number_list:
                    if is_valid(board, row, col, number):
                        board[row][col] = number
                        if not is_empty(board):
                            return True
                        else:
                            if self.create_board(board):
                                return True
                break
        board[row][col] = 0
        return False

    # Get a list of filled positions and return list shuffle
    def get_filled_pos_list(self, board):
        filled_pos_list = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 0:
                    filled_pos_list.append((i, j))
        shuffle(filled_pos_list)
        return filled_pos_list

    # Function to remove some positions from full board
    def remove_numbers_from_board(self):
        # Get a list of filled spots
        filled_pos_list = self.get_filled_pos_list(self.board)
        filled_count = len(filled_pos_list)
        rounds = 3
        while rounds > 0 and filled_count >= 17:
            # Must be at least 17 filled spots
            row, col = filled_pos_list.pop()
            filled_count -= 1
            # Hold a value if there is more than one solution later on
            temp = self.board[row][col]
            self.board[row][col] = 0
            # Make a copy of board
            board_copy = copy.deepcopy(self.board)
            # Initialize solutions counter
            self.counter = 0
            self.solve_puzzle(board_copy)
            # If there is more than one solution, not remove it and move on to next one
            if self.counter != 1:
                self.board[row][col] = temp
                filled_count += 1
                rounds -= 1


if __name__ == "__main__":
    sudoku = SudokuGenerator()
    temp = sudoku.original_board
    for v in temp:
        print(v)
