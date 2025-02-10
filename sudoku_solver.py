class TreeNode:
    #time complexity for __init__ is O(n^2), as it makes a copy of the board
    def __init__(self, board, row=-1, col=-1, num=None):
        self.board = [row[:] for row in board]  # makes copy the right way, "=" doesnt work
        self.children = []
        
        
        if num is not None and row != -1 and col != -1:
            self.board[row][col] = num


class SudokuSolver:
    #time complexity for __init__ is O(n^2), as it makes a copy of the board, best case scenario is O(1) w, 
    def __init__(self, board):
        self.root = TreeNode(board) # board = the initial state to be solved
        self.size = 9
        self.subgrid_size = 3
    
    #time complexity for is_valid is O(n), best case scenario is O(1) when the number is in the first row or column, worst case scenario is O(n) when the number is not in the row or column or subgrid.
    def is_valid(self, board, row, col, num): # checks if a number can be placed at board[row][col] without conflicts 
    
        for i in range(self.size):
            if board[row][i] == num:
                return False

        for i in range(self.size):
            if board[i][col] == num:
                return False

        start_row = row - row % self.subgrid_size
        start_col = col - col % self.subgrid_size
        for i in range(self.subgrid_size): #seems that it could be O(n^2) but it is not, it is o(n) as the subgrid_size is always 3, which is the square root of the size of the board (sqrt(n)*sqrt(n) = n)
            for j in range(self.subgrid_size):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True

    #time complexity for find_empty_cell is O(n^2). Best case scenario is O(1) when the first cell is empty, worst case scenario is O(n^2) when it is full.
    def find_empty_cell(self, board):
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    return row, col # returns a tuple!!
        return None

    #time complexity for dfs is O(n^(n^2)), it is so high because it is a backtracking algorithm
    #best case scenario is O(n^2) when the sudoku is already solved, worst case scenario is O(n^(n^2)) when the sudoku is empty, average case scenario is O(n^(n^2))
    def dfs(self, node):

        #base case (sudoku is solved)
        empty_cell = self.find_empty_cell(node.board)
        if not empty_cell:
            return True  

        row, col = empty_cell

        for num in range(1, self.size + 1):
            if self.is_valid(node.board, row, col, num):
                child_node = TreeNode(node.board, row, col, num)
                node.children.append(child_node)
                
                #recursive part
                if self.dfs(child_node):
                    node.board = child_node.board  #the result is saved in the class, no need to return
                    return True

                #this clears the worng paths if the number is not valid
                node.children.remove(child_node)

        # We will add only valid sudokus but in case we make a mistake it will show here
        return False

    def solve_sudoku(self): #for code clarity
        return self.dfs(self.root)