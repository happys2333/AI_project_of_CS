#code:utf-8
#author:zkl
import numpy as np
import pygame
from pygame.locals import *
from enum import Enum

#颜色RGB
class Color(Enum):
    WHIHT = (255,255,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
#棋子类
class chess():
    #初始化
    def __init__(self):
        pass
    #接受位置和颜色
    def set_pos(self,pos):
        self.pos = pos
    def get_pos(self,pos):
        return self.pos
    # 传出位置和颜色
    def set_color(self,color):
        self.color = color
    def get_color(self,color):
        return self.color
# 棋盘类
class Chessboard():
    #棋盘颜色，记录当前谁走
    chessboardBorW = -1
    #行数和列数SIZE
    SIZE = 10
    #单元格大小UNIT
    UNIT = 35
    #记录当前棋盘状态:二维数组，-1~黑棋，0~无棋，1~白棋
    chessmap = np.zeros((SIZE,SIZE), dtype = int)
    #初始化棋盘
    def __init__(self,size,unit):
        self.SIZE = size
        self.UNIT = unit
    # 绘制棋盘, 传入当前棋盘，窗口，边框宽度
    def drawchessboard(self,screen, width):
        # 行
        for row in range(self.SIZE):
            pygame.draw.line(screen, Color.RED.value,
                             (width, width + row * self.UNIT),
                             (width + self.UNIT * (self.SIZE - 1),
                              width + row * self.UNIT))
        # 列
        for column in range(self.SIZE):
            pygame.draw.line(screen, Color.RED.value,
                             (width + column * self.UNIT, width),
                             (width + column * self.UNIT,
                              width + self.UNIT * (self.SIZE - 1)))
# 主程序
#初始化界面


class init_game():
    # 设置边框宽度
    BOARD_WIDTH = 50
    # 创建棋盘
    chessboard = Chessboard(10, 35)
    pygame.init()
    #记录步数,成员为(颜色，[位置])例（1，[x,y]）
    his_stack = []
    # 创建窗口
    screen = pygame.display.set_mode((2*BOARD_WIDTH+chessboard.UNIT*(chessboard.SIZE - 1),
                                      2*BOARD_WIDTH+chessboard.UNIT*(chessboard.SIZE - 1)))
    #设置窗口标题
    pygame.display.set_caption("我的五子棋AI果然有问题")
    #设置背景
    background = pygame.image.load('bg.jpg')
    screen.blit(background,(-100,-100))
    #绘制棋盘
    chessboard.drawchessboard(screen,BOARD_WIDTH)
    #绘制棋子
    def drawchess(self):
        for item in self.his_stack:
            #判断当前棋子颜色
            c = Color.BLACK.value
            if item[0] == 1:
                c = Color.WHIHT.value
            pygame.draw.circle(self.screen, c,
                               (self.BOARD_WIDTH + self.chessboard.UNIT * item[1][0],
                                self.BOARD_WIDTH + self.chessboard.UNIT * item[1][1]),
                               int(self.chessboard.UNIT/2.5))
            #更改棋盘信息
            self.chessboard.chessmap[item[1][0]][item[1][1]] = item[0]
            # #检测是否更改棋盘信息
            # print(self.chessboard.chessmap[item[1][0]][item[1][1]])
    #move，检测步数
    def move(self,pos):
        #判断光标点击是否有效
        if pos[0] < self.BOARD_WIDTH \
                or pos[0] > self.BOARD_WIDTH + self.chessboard.UNIT * (self.chessboard.SIZE - 1)  \
                or pos[1] < self.BOARD_WIDTH \
                or pos[1] > self.BOARD_WIDTH + self.chessboard.UNIT * (self.chessboard.SIZE - 1):
            return
        else:
            # 像素转化为坐标
            x = round((pos[0] - self.BOARD_WIDTH) / self.chessboard.UNIT)
            y = round((pos[1] - self.BOARD_WIDTH) / self.chessboard.UNIT)
            # 判断是否可以落子
            if (self.chessboard.chessmap[x][y] != 0):
                return
            else:
                #人落子
                self.his_stack.append((self.chessboard.chessboardBorW, [x, y]))
                init_game.drawchess(newgame)
                #判断是否获胜 PS如果获胜，当前还未终止游戏，需后期修改
                if self.iswin(x,y):
                    print("玩家获胜！")
                #修改当前谁走
                if self.chessboard.chessboardBorW == 1:
                    self.chessboard.chessboardBorW = -1
                else:
                    self.chessboard.chessboardBorW = 1
                print ("person")
                print(self.chessboard.chessboardBorW)
                #ai落子
                self.his_stack.append((self.chessboard.chessboardBorW,self.getaimove()))
                init_game.drawchess(newgame)
                #判断是否获胜 PS如果获胜，当前还未终止游戏，需后期修改
                if self.iswin(self.getaimove()[0],self.getaimove()[1]):
                    print("AI获胜！")
                # 修改当前谁走
                if self.chessboard.chessboardBorW == 1:
                    self.chessboard.chessboardBorW = -1
                else:
                    self.chessboard.chessboardBorW = 1
                print("ai")
                print(self.chessboard.chessboardBorW)
    #aimove
    def getaimove(self):
        for i in range(self.chessboard.SIZE):
            for j in range(self.chessboard.SIZE):
                if self.chessboard.chessmap[i][j] == 0:
                    posx = i
                    posy = j
                    break
        return (posx,posy)
    #判断是否获胜,pos为当前步，计算连续棋子数
    def iswin(self,posx,posy):
        count = 0
        #同行
        #同行右侧
        for i in range(posx,self.chessboard.SIZE):
            if self.chessboard.chessmap[posx][posy] == self.chessboard.chessboardBorW:
                count = count + 1
            else:
                break
        #同行左侧
        for i in range(0,posx):
            if self.chessboard.chessmap[posx][posy] == self.chessboard.chessboardBorW:
                count = count + 1
            else:
                break
        #判断输赢
        if count >= 5:
            return True
        else:
            count = 0
        #同列
        #同列下侧
        for i in range(posy,self.chessboard.SIZE):
            if self.chessboard.chessmap[posx][posy] == self.chessboard.chessboardBorW:
                count = count + 1
            else:
                break
        #同列上侧
        for i in range(0,posy):
            if self.chessboard.chessmap[posx][posy] == self.chessboard.chessboardBorW:
                count = count + 1
            else:
                break
        #判断输赢
        if count >= 5 :return True
        else:count = 0
        #右下
        for i in range(posx,self.chessboard.SIZE):
            for j in range(posy,self.chessboard.SIZE):
                if self.chessboard.chessmap[posx][posy] == self.chessboard.chessboardBorW:
                    count = count + 1
                else:
                    break
        #左上
        for i in range(0,posx):
            for j in range(0,posy):
                if self.chessboard.chessmap[posx][posy] == self.chessboard.chessboardBorW:
                    count = count + 1
                else:
                    break
        #判断输赢
        if count >= 5:
            return True
        else:
            count = 0
        #左下
        for i in range(0,posx):
            for j in range(posy, self.chessboard.SIZE):
                if self.chessboard.chessmap[posx][posy] == self.chessboard.chessboardBorW:
                    count = count + 1
                else:
                    break
        #右上
        for i in range(posx,self.chessboard.SIZE):
            for j in range(0,posy):
                if self.chessboard.chessmap[posx][posy] == self.chessboard.chessboardBorW:
                    count = count + 1
                else:
                    break
        #判断输赢
        if count >= 5:
            return True
        else:
            return False

#控制游戏进程
if __name__ == '__main__':
    newgame = init_game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONUP:
                init_game.move(newgame,event.pos)
        pygame.display.update()