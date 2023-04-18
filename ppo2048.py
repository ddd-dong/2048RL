import pygame
import random
import numpy as np
import gym
from gym import spaces
import time
import matplotlib.pyplot as plt

class Game2048:
    
    def __init__(self) -> None:
        pygame.init()#初始化
        super(Game2048,self).__init__()
        self.score=0
        self.movetime=0
        self.N = 4#棋盤成數4x4
        self.cellSize = 100#每個單元格的大小
        self.gap = 5#間隔大小
        self.windowBgColor = (180, 170, 160)#遊戲窗口背景顏色
        self.blockSize = self.cellSize + self.gap * 2#這是每個方塊（單元格 + 間隔）的大小
        self.BG_COLORS = {#字典
            0: (250, 250, 250),
            2: (238, 228, 218),
            4: (238, 225, 201),
            8: (243, 178, 122),
            16: (246, 150, 100),
            32: (247, 124, 95),
            64: (247, 95, 59),
            128: (237, 208, 115),
            256: (237, 204, 98),
            512: (237, 201, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        self.windowWidth = self.blockSize * 4
        self.windowHeight = self.windowWidth

        
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))#長寬
        self.myFont = pygame.font.SysFont("Helvectia", 48,"bold")#字體
        pygame.display.set_caption("2048")#標題為“2048”。

        self.boardStatus = np.zeros((self.N, self.N))#設置為一個4x4的零矩陣
        self.addNewNumber() # 加2
        self.addNewNumber()
    
    def addNewNumber(self):
        freePos = zip(*np.where(self.boardStatus == 0))#找到0的位置用zip轉成列表
        freePos = list(freePos)#列表

        for pos in random.sample(freePos, k=1):#隨機選擇一個位置 k=選的數量
            self.boardStatus[pos] = 2#設置成2

    def drawBoard(self):
        self.window.fill(self.windowBgColor)

        for r in range(self.N):
            rectY = self.blockSize * r + self.gap
            for c in range(self.N):
                rectX = self.blockSize * c + self.gap
                cellValue = int(self.boardStatus[r][c])#51~55在每個單元格上繪製一個大小為100矩形在每個單元格周圍留下5的間格大小
                if cellValue in self.BG_COLORS:#取德每個單元格的值如果值在字典中填充為對應的顏色
                    pygame.draw.rect(
                        self.window,
                        self.BG_COLORS[cellValue],
                        pygame.Rect(rectX, rectY, self.cellSize, self.cellSize)
                    )
                else:
                    pygame.draw.rect(
                        self.window,
                        self.BG_COLORS[2],
                        pygame.Rect(rectX, rectY, self.cellSize, self.cellSize)
                    )
                if cellValue != 0:
                    textSurface = self.myFont.render(f"{cellValue}", True, (0, 0, 0))
                    textRect = textSurface.get_rect(center=(rectX + self.blockSize/2, rectY + self.blockSize/2))
                    self.window.blit(textSurface, textRect)#68~71如果數字=0，用 self.myFont.render 方法將該值放到單元格中心

    def compressNumber(self, data):#壓縮數字 下面用到 傳入一個代表了一行棋盤數字列表
        
        result = [0]
        data = [x for x in data if x != 0]#遍歷 data 列表 過濾0舊表[2,0,0,2]->新表[2,2]。懶的解釋      
        for element in data:
            if element == result[len(result) - 1]:
                result[len(result) - 1] *= 2 
                self.score=self.score+1
                result.append(0)
            else:
                result.append(element)
        #如果該元素等於列表中最後一個元素[2,2]，則將列表中最後一個元素乘以2[4,2]，然後將 0 添加到 result 列表中否則[4,0]，將該元素添加到 result 列表中。
        result = [x for x in result if x != 0]
        return result

    def move(self, dir):
        
        for idx in range(self.N):

            if dir in "UD":#判斷是移動方向為垂直或水平看曲航還是列
                data = self.boardStatus[:, idx]
            else:
                data = self.boardStatus[idx, :]

            flip = False#不用轉
            if dir in "RD":#如果是向右或向下移動，則需要先將數據反轉，將相鄰的相同元素合併成一個。
                flip = True
                data = data[::-1]

            data = self.compressNumber(data)#將返回一個新的合併數組
            data = data + (self.N - len(data)) * [0]#數據的末尾添加一些0

            if flip:#如果轉了
                data = data[::-1]#將數據反轉回來
            if dir in "UD":#根據移動方向，將更新後的數據重新存儲
                self.boardStatus[:, idx] = data
            else:
                self.boardStatus[idx, :] = data


    def play_ai(self,action:str):
        self.drawBoard()
        pygame.display.update()
        oldBoardStatus = self.boardStatus.copy()
        self.move(action)
        if (self.boardStatus == oldBoardStatus).all() == False:
                        self.addNewNumber()

    def get_observation(self)->list:
        #回傳當前的map    
        return self.boardStatus

        
    def isend(self)->bool:# 回傳遊戲是否已結束
        boardStatusBackup = self.boardStatus.copy()#建立一個目前遊戲狀態的備份，便於後面的還原操作。
        for dir in "UDLR":#迴圈遍歷上下左右
            self.move(dir)#調用 move() 方法，將當前遊戲狀態向指定方向移動一步

            if (self.boardStatus == boardStatusBackup).all() == False:
                self.boardStatus = boardStatusBackup
                
                return False #如果移動後的狀態和備份的狀態一致，表示當前的遊戲狀態已經無法再移動，還原備份的狀態
        print("end!!")
        # print(boardStatusBackup,2 in self.boardStatus)
        return True#不然就繼續執行


    def reset(self)->None:
        self.score=0
        self.movetime=0
        pygame.init()
        self.boardStatus = np.zeros((self.N, self.N))
        self.addNewNumber()
        self.addNewNumber()

class Game2048Env(gym.Env,Game2048):

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        self.env = Game2048()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=44096709674720289, shape=(16,), dtype=np.float64)
        self._actions=["U","D","L","R"]
        
    def reset(self)->list:
        print("New")
        self.env.reset()
        _observation = self.env.get_observation()
        _obvout = _observation[0]
        for i in range(1,4):
            _obvout = np.append(_obvout,_observation[i])
        # print(type(_obvout),type(_obvout[0]),_obvout,_observation)
        return _obvout
    
    def step(self,action:int):
        # surface = pygame.display.get_surface()
        # pxarray = pygame.PixelArray(surface)
        # arr = np.array(pxarray)
        # pxarray.close()
        # imgdata = pygame.surfarray.array3d(pygame.surfarray.make_surface(arr))

        # # 顯示RGB數組
        # plt.imshow(imgdata)
        # plt.show()
        time.sleep(0.1)
        old_score=self.env.score
        if action < 4: 
            self.env.play_ai(self._actions[action])
        else:
            raise ValueError("Invalid action")
        _observation = self.env.get_observation()
        _obvout = _observation[0]
        for i in range(1,4):
            _obvout = np.append(_obvout,_observation[i])
        pygame.event.pump()
        if 2048 in self.env.boardStatus:
            print("Win")
            return _obvout,20,True,{}
        if self.env.isend():
            print("dead")
            # print(self.env.score)
            return _obvout,-10,self.env.isend(),{}
        # print(self.env.score-old_score)
        return _obvout,self.env.score-old_score,self.env.isend(),{}
    
    def render(mode='human'):
        # print("AAA_A")
        pass

    def close(self):
        print("colse")
        pygame.event.pump()
        pass

