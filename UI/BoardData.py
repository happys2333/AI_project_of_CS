#author:白炎拉力

import numpy as np
from enum import Enum


class Chess(Enum):
    White = 1
    Black = -1


class BoardData:
    # in array board, 1 means white chess, -1 means black chess, 0 means nothing
    thisTurn = False  # this turn is true when it's white chess ready to put

    def __init__(self, row, column):
        self.row = row
        self.column = column
        print([row,column])
        self.board = np.zeros((row, column), dtype=int)

    def getBoard(self):
        print(self.board)
        return self.board

    def putChess(self, row, column):
        if row>=self.row or column>=self.column or row< 0 or column < 0:
            return False
        if self.board[row, column] == 0:
            if self.thisTurn:
                self.board[row, column] = 1
            else:
                self.board[row, column] = -1
            if self.checkWin(row, column):
                return True
            self.thisTurn = not self.thisTurn
        else:
            return False

    def checkWinAll(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                if self.checkWin(row, column):
                    return True
        return False

    def checkWin(self, row, column):
        color = self.board[row, column]
        directions = ((1, 0), (0, 1), (1, 1), (1, -1))
        if(color==0): return False
        for direction in directions:
            count = 1
            step = 1
            while self.inBound(row + direction[0] * step, column + direction[1] * step) and color == self.board[
                row + direction[0] * step, column + direction[1] * step]:
                count += 1
                step += 1
                if count == 5: return True
            step = 1
            while self.inBound(row - direction[0] * step, column - direction[1] * step) and color == self.board[
                row - direction[0] * step, column - direction[1] * step]:
                count += 1
                step += 1
                if count == 5: return True

    def inBound(self, row, column):
        if 0 <= row < len(self.board) and 0 <= column < len(self.board[0]):
            return True
        else:
            return False



if __name__ == '__main__':
    board = BoardData(5, 5)
    for i in range(5):
        board.putChess(0, i)
        print(board.checkWinAll())
        board.putChess(1, i)
        board.getBoard()
