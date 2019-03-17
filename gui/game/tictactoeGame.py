import numpy as np

class TicTacToeGame:
    def __init__(self):
        self.grid = np.zeros(9, dtype=np.chararray)
        self._availableMoves = 9

    def updateGrid(self, grid_position, symbol):
        valid = self.grid[grid_position] == 0
        if valid:
            self.grid[grid_position] = symbol
            self._availableMoves -= 1

        return valid

    def getAvailableMoves(self):
        return self._availableMoves

    def hasWon(self):
        side = int(np.sqrt(len(self.grid)))

        # rows
        for x in range(0,3):
            row = set([self.grid[(x * side) + 0], self.grid[(x * side) + 1], self.grid[(x * side) + 2]])
            if len(row) == 1 and self.grid[(x * side)] != 0:
                return self.grid[(x * side)]

        # columns
        for x in range(0,3):
            column = set([self.grid[(0 * side) + x], self.grid[(1 * side) + x], self.grid[(2 * side) + x]])
            if len(column) == 1 and self.grid[0 + x] != 0:
                return self.grid[0 + x]

        # diagonals
        diag1 = set([self.grid[(0 * side) + 0], self.grid[(1 * side) + 1], self.grid[(2 * side) + 2]])
        diag2 = set([self.grid[(0 * side) + 0], self.grid[(1 * side) + 1], self.grid[(2 * side) + 2]])
        if len(diag1) == 1 or len(diag2) == 1 and self.grid[(1 * side) + 1] != 0:
            return self.grid[(1 * side) + 1]

        return False

    def getPlayerFromSymbol(self, symbol):
        return 1 if symbol == 'X' else 2
        

    def playerPicks(self, playerNumber, grid_position):
        return self.updateGrid(grid_position, self.getPlayerSymbol(playerNumber))

    def getPlayerSymbol(self, playerNumber):
        return 'X' if playerNumber % 2 == 1 else 'O'

    def getSymbol(self, position):
        if position >= 0 and position < len(self.grid):
            return self.grid[position]