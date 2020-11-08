import copy
import math
import sys


class SudokuBoard(object):
    CHARSET = frozenset('123456789')
    EMPTY = '.'
    BOARD_SIZE = len(CHARSET)
    SUBSQUARE_SIZE = int(math.sqrt(BOARD_SIZE))
    
    
    def __init__(self, board, position_possible_values=None):
        self._board = copy.deepcopy(board)
        
        if position_possible_values:
            self._position_possible_values = copy.deepcopy(position_possible_values)
        else:
            self._position_possible_values = {(x,y) : self.getPossibleValues(x,y) for x in range(self.BOARD_SIZE) for y in range(self.BOARD_SIZE) if self.isEmptyPosition(x,y)}
    
    
    def __hash__(self):
        return hash(''.join((''.join(row) for row in self._board)))
    
    
    def __str__(self):
        return str(self._board)
    
    def getBoard(self):
        return self._board
    
    def getAllPositionValues(self):
        return self._position_possible_values
    
    def getNextMovePositionValues(self):
        assert self.isValidSudoku()
        
        best_position = None
        best_values = None

        for position, values in self._position_possible_values.items():
            if not best_values or len(values) < len(best_values):
                best_values = values
                best_position = position
                
        return (best_position, best_values)
        
    
    def isValidSudoku(self):
        for possible_values in self._position_possible_values.values():
                # Invalid if any position doesn't have any possible value to fill it
                if not possible_values:
                    return False
        return True
    
    def isFinishedSudoku(self):
        if not self.isValidSudoku():
            return False
        
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if self.isEmptyPosition(x,y):
                    return False
        return True
    
    
    def getSubsquarePositions(self, i, j):
        """Returns an iterable that contains all the subsquare's positions containing (i,j)"""
        subsquare_i = i // self.SUBSQUARE_SIZE
        subsquare_j = j // self.SUBSQUARE_SIZE
        return ((x,y) for x in range(self.SUBSQUARE_SIZE*subsquare_i, self.SUBSQUARE_SIZE*(subsquare_i+1)) for y in range(self.SUBSQUARE_SIZE*subsquare_j, self.SUBSQUARE_SIZE*(subsquare_j+1)))
    
    
    def isEmptyPosition(self, i, j):
        return self.getPosition(i,j) == self.EMPTY
    
    
    def getPosition(self, i, j):
        return self._board[i][j]
    
    
    def setPosition(self, position, value):
        assert len(position) == 2
        assert self._setPosition(position[0], position[1], value)
        
        
    def _setPosition(self, i, j, value):
        """set board position at (i,j) and returns if setting is successful."""
        if self.isEmptyPosition(i,j):
            self._board[i][j] = value
            
            # Remove (i,j)'s entry from position_possible_values
            del self._position_possible_values[(i,j)]
            for position, values in self._position_possible_values.items():
                # Discarding value from i'th row and j'th column
                if position[0] == i or position[1] == j:
                    self._position_possible_values[position].discard(value)
                # Discard value from (i,j)'s subsquare
                elif (position[0] // self.SUBSQUARE_SIZE) == (i // self.SUBSQUARE_SIZE) and \
                     (position[1] // self.SUBSQUARE_SIZE) == (j // self.SUBSQUARE_SIZE):
                    self._position_possible_values[position].discard(value)
                
            return True
        return False
    
    
    def getPossibleValues(self, i, j):
        """Returns a set of all possible values at position (i, j)."""
        assert self.isEmptyPosition(i, j)
        horizontal_values = \
            {self.getPosition(i, x) for x in range(self.BOARD_SIZE) \
             if not self.isEmptyPosition(i,x)}
        vertical_values = \
            {self.getPosition(x, j) for x in range(self.BOARD_SIZE) \
             if not self.isEmptyPosition(x, j)}
        
        subsquare_values = set()
        for (x,y) in self.getSubsquarePositions(i,j):
                if not self.isEmptyPosition(x,y):
                    subsquare_values.add(self.getPosition(x,y))
                    
        return set(self.CHARSET) - (horizontal_values | vertical_values | subsquare_values)
        
def copySolution(solution_board, output_board):
    assert len(solution_board) == len(output_board)
    assert len(solution_board[0]) == len(output_board[0])
    for i in range(len(solution_board)):
        for j in range(len(solution_board[i])):
            output_board[i][j] = solution_board[i][j]
        
class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        initial_board = SudokuBoard(board)
        assert initial_board.isValidSudoku()
        
        if initial_board.isFinishedSudoku():
            return
        
        # All boards in the stack should be valid boards.
        dfs_stack = [initial_board]
        visited_boards_hashes = set()
        
        
        while dfs_stack:
            current_board = dfs_stack.pop()
            # print(f'Current board is \n{current_board}\n')
            visited_boards_hashes.add(hash(current_board))
            
            (next_position, next_values) = current_board.getNextMovePositionValues()
            valid_board = True
                
            # These are the sure positions
            while len(next_values) == 1:
                value = next(iter(next_values))
                # print(f'Setting sure value {value} at position {next_position}')
                current_board.setPosition(next_position, value)
                if not current_board.isValidSudoku():
                    valid_board = False
                    break
                    
                if current_board.isFinishedSudoku():
                    # print(f'Solution found: {current_board}\n')
                    copySolution(current_board.getBoard(), board)
                    return
                
                (next_position, next_values) = current_board.getNextMovePositionValues()
                
            if not valid_board or not next_values:
                # print(f'Is valid board {valid_board}. next_values are {next_values}')
                continue
            
            # print(f'Next values are {next_values} at position {next_position}')
    
            for value in next_values:
                # print(f'Setting value {value} at position {next_position}')
                next_board = SudokuBoard(current_board.getBoard(), 
                                         current_board.getAllPositionValues())
                next_board.setPosition(next_position, value)
                if not next_board.isValidSudoku():
                    continue
                elif hash(next_board) not in visited_boards_hashes:
                    if next_board.isFinishedSudoku():
                        # print(f'Solution found: {next_board}\n')
                        copySolution(next_board.getBoard(), board)
                        return
                    dfs_stack.append(next_board)
                    
                    
