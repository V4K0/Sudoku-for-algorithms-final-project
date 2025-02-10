import puzzles
import sudoku_solver

LEVEL_LIVES = 3

#time complexity for get_sudoku is O(1), as it is a dictionary lookup
def get_sudoku(level):
    sudoku_puzzles = puzzles.sudoku_puzzles #dictionary of sudoku puzzles
    return sudoku_puzzles.get(level, "Invalid level. Choose a level between 1 and 10.")

#time complexity for solve_sudoku_puzzle is O(n^n^2).
def solve_sudoku_puzzle(grid):
    solver = sudoku_solver.SudokuSolver([row[:] for row in grid])  #deep copy needed, "=" does not work beacuse it is a reference and with self.board = board it will change the original board
    solver.solve_sudoku()
    return solver.root.board

# time complexity for initialize_lives is O(1)
def initialize_lives():
    # This function can be modified to return different number of lives based on the level. We prefer to do it this way to keep the code simple.
    return LEVEL_LIVES

#time complexity for is_valid_move is O(1)
def is_valid_move(grid, solution_grid, row, col, num):
    #check if the number is valid in the row, column, and 3x3 grid by comparing the current grid with the solved grid.
    return grid[row][col] == 0 and solution_grid[row][col] == num

#time complexity for is_puzzle_complete is O(n^2)
def is_puzzle_complete(grid):
    #check if the puzzle is complete by checking if there are any empty cells (zeroes) left in the grid.
    return all(0 not in row for row in grid)

#time complexity for calculate_score is O(1)
def calculate_elapsed_time(start_time, end_time):
    #calculate the elapsed time in hours, minutes, and seconds.
    elapsed_time = end_time - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return int(hours), int(minutes), int(seconds)