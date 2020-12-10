# code:utf-8
# author:zkl,白炎
from time import sleep

import pygame
import tkinter
import tkinter.messagebox
from pygame.locals import *
from enum import Enum


# 颜色RGB

from UI import BoardData


class Color(Enum):
    WHITE = 0
    BLACK = 1
    RED = (255, 0, 0)


# 棋子类
class chess():
    # 初始化
    def __init__(self, screen, color, row, column):
        self.screen = screen
        self.image = pygame.image.load("AI/Images/chess" + str(color.value) + ".png")
        self.image = pygame.transform.scale(self.image, (Chessboard.UNIT * 2, Chessboard.UNIT * 2))
        self.pos = Chessboard.convertArrayToPos(row, column)
        self.rect = self.image.get_rect()
        self.rect = self.pos
        self.screen.blit(self.image, self.rect)


# 棋盘类
class Chessboard:

    # 初始化棋盘
    def __init__(self, board_data, UNIT=35, width=50):
        self.ROW = board_data.row
        self.COLUMN = board_data.column
        Chessboard.UNIT = UNIT
        Chessboard.width = width

    # 绘制棋盘, 传入当前棋盘，窗口，边框宽度
    def drawmap(self, screen, width):

        # 行
        for row in range(self.COLUMN):
            pygame.draw.line(screen, Color.RED.value,
                             (width, width + row * self.UNIT),
                             (width + self.UNIT * (self.ROW - 1),
                              width + row * self.UNIT))
        # 列
        for column in range(self.ROW):
            pygame.draw.line(screen, Color.RED.value,
                             (width + column * self.UNIT, width),
                             (width + column * self.UNIT,
                              width + self.UNIT * (self.COLUMN - 1)))

    @staticmethod
    def convertArrayToPos(row, column):
        return Chessboard.width + (row - 1) * Chessboard.UNIT, Chessboard.width + (column - 1) * Chessboard.UNIT

    @staticmethod
    def convertPosToArray(x, y):
        return (x - Chessboard.width // 2) // Chessboard.UNIT, (y - Chessboard.width // 2) // Chessboard.UNIT

class bboard:
    def __init__(self,boardData):
        self.boardData=boardData


# 主程序
# 初始化界面


screen = 1

def set_human(human):
    global Human
    Human=human

def init_game():
    # 设置边框宽度
    BOARD_WIDTH = 50
    # 创建棋盘
    global boardData
    boardData = BoardData.BoardData(8, 8)
    chessBoard = Chessboard(boardData)
    pygame.init()

    SIZE = (2 * BOARD_WIDTH + chessBoard.UNIT * (chessBoard.ROW - 1),
            2 * BOARD_WIDTH + chessBoard.UNIT * (chessBoard.COLUMN - 1))
    # 创建窗口
    global screen
    screen = pygame.display.set_mode(SIZE)
    # 设置窗口标题
    pygame.display.set_caption("我的五子棋AI果然有问题")
    # 设置背景
    background = pygame.image.load('AI/Images/bg.jpg')
    background = pygame.transform.scale(background, SIZE)

    screen.blit(background, (0, 0))
    # #绘制棋盘
    # Chessboard.drawmap(screen,BOARD_WIDTH)
    chessBoard.drawmap(screen, 50)

    pygame.display.update()

def updateBoard(board):
    if boardData:
        boardData.transportToBoardData(board)
        showChess()


# To solve mouse click event
def checkEvent(event):
    if event.type == MOUSEBUTTONDOWN:
        row, column = Chessboard.convertPosToArray(event.pos[0], event.pos[1])
        putChessOnBoard(row, column)
        pygame.display.update()
    pass


def putChessOnBoard(row, column):
    # pass
    print(row,column)
    if Human!=None:
        Human.give_input(boardData.row-1-column,row)
    # Human.give_input(row,column)
    # isWin = boardData.putChess(row, column)
    # if isWin != False:
    #     chessNew = chess(screen, Color.WHITE if boardData.thisTurn else Color.BLACK, row, column)
    #     print(row,column)
    # print(isWin)
    # if isWin:
    #     tkinter.messagebox.askokcancel(title="Who Won?", message="White won" if boardData.thisTurn else "Black won");
    #     init_game()
    # return isWin

def showChess():
    for i in range(boardData.row):
        for j in range(boardData.column):
            if boardData.getBoard()[i][j]==1:
                chessNew=chess(screen, Color.WHITE , i, j)
            elif boardData.getBoard()[i][j]==-1:
                chessNew = chess(screen, Color.BLACK, i, j)
    pygame.display.update()


# 控制游戏进程
def open_UI():

    # init_game()
    while True:
        sleep(0.5)
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            else:
                checkEvent(event)


if __name__=="__main__":
    open_UI()