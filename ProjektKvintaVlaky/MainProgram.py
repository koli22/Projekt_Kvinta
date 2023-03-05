import pygame
from pygame.locals import *
import random
from OtherScripts.getInputLetter import getLetter
from OtherScripts.makePaths import MakePaths
import os
import sys
import time

class MainClass:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Train Simulator')
        pygame.font.init() 
        self.velikostX = 500
        self.velikostY = 500
        self.screen = pygame.display.set_mode((self.velikostX,self.velikostY), RESIZABLE)
        self.settings = self.ReadSettings()
        self.CreateBoard()
        self.LoadImages()
        self.offset = [0,0]
        self.gIL = getLetter()
        
        self.pressedUP = False
        self.pressedDOWN = False
        self.pressedLEFT = False
        self.pressedRIGHT = False 
        
        self.picked = 0
        self.selectedSquare = 0
        self.rotation = 0
        
        self.mousePosition = (0,0)
        self.clicked = False
        self.running = True
        self.pickedTrain = 0
        
        self.simulaceON = False
        self.font = pygame.font.Font("textures/"+self.settings[1]+"/"+"Shelpy.otf", 32)
        self.selectedTrain = 0
        
        self.makePaths = MakePaths()
        self.ctrl = False
        
        
        
        self.GameLoop()
        
        
    def GameLoop(self):
        while self.running:
            self.GetInputs()
            self.MoveOnBoard()
            if self.clicked == True:
                self.Place()
            if self.settings[5] == "True":
                if random.randint(1,10000) == 1:
                    self.growTrees()
            self.Draw()
        pygame.display.quit()
        
    def askForSave(self):
        text = ""
        running = True
        self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"askForSave"+".png"),((self.velikostX-300)/2,(self.velikostY-200)/2))
        while running:
            inputs = self.gIL.gL(pygame.event.get())
            for i in range(len(inputs)):
                if inputs[i] == -2:
                    running = False
                elif inputs[i] == -1:
                    if len(text)>0:
                        running = False
                        if os.path.exists("savesFile/"+text+".txt"):
                            os.remove("savesFile/"+str(self.nameoffile)+".txt")
            
                        f = open("savesFile/"+text+".txt", "a")
                        for i in range(len(self.positions)):
                            f.write(str(self.positions[i][0][0])+","+str(self.positions[i][0][1])+" "+str(self.positions[i][1][0])+","+str(self.positions[i][1][1])+","+str(self.positions[i][1][2])+","+str(self.positions[i][1][3])+","+str(self.positions[i][1][4])+","+str(self.positions[i][1][5]))
                            if (len(self.positions)-1 > i):
                                f.write("\n")
                            else:
                                f.write(" ")
                        f.close()
                elif inputs[i] == -3:
                    if len(text) > 0:
                        text = text[:-1]
                else:
                    if len(text) < 20:
                        text += inputs[i]
            self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"askForSave"+".png"),((self.velikostX-300)/2,(self.velikostY-200)/2))
            text_surface = self.font.render(text+".txt", False, (0, 0, 0))
            self.screen.blit(text_surface, ((self.velikostX-300)/2+35,(self.velikostY-200)/2+140))
            pygame.display.flip()
        if self.settings[5] == "True":
            self.growTrees()
        self.Draw()
        
        
    def askForLoad(self):
        text = ""
        running = True
        self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"askForLoad"+".png"),((self.velikostX-300)/2,(self.velikostY-200)/2))
        while running:
            inputs = self.gIL.gL(pygame.event.get())
            for i in range(len(inputs)):
                if inputs[i] == -2:
                    running = False
                elif inputs[i] == -1:
                    if len(text) > 0:
                        running = False
                        if os.path.exists("savesFile/"+text+".txt"):
                            lines = open("savesFile/"+text+".txt", "r").readlines()
                            self.trees = []
                            for i in range(len(lines)):
                                if lines[i][:-2] == "\n":
                                    lines[i] = lines[:-2]
                                    
                                line = lines[i].split(" ")
                                xy = line[0].split(",")
                                other = line[1].split(",")
                                
                                for i in range(len(other)):
                                    other[i] = int(other[i])
                                    
                                self.positions[self.itoxy[int(xy[0])][int(xy[1])]] = [[int(xy[0]),int(xy[1])],[other[0],other[1],other[2],other[3],other[4],other[5]]]
                                if self.positions[self.itoxy[int(xy[0])][int(xy[1])]][1][-2] == 2:
                                    self.trees.append([int(xy[0]),int(xy[1]),other[5]])
                                    
                elif inputs[i] == -3:
                    if len(text) > 0:
                        text = text[:-1]
                else:
                    if len(text) < 20:
                        text += inputs[i]
            self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"askForLoad"+".png"),((self.velikostX-300)/2,(self.velikostY-200)/2))
            text_surface = self.font.render(text+".txt", False, (0, 0, 0))
            self.screen.blit(text_surface, ((self.velikostX-300)/2+35,(self.velikostY-200)/2+140))
            pygame.display.flip()
        if self.settings[5] == "True":
            self.growTrees()
        self.Draw()
                
    def Draw(self):
        self.screen.fill((0,0,0))
        for i in range(len(self.positions)):
            self.screen.blit(self.dekorace[self.positions[i][1][4]][self.positions[i][1][5]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
            if self.positions[i][1][0] == 3:
                self.screen.blit(self.squares[1][self.positions[i][1][1]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
            self.screen.blit(self.squares[self.positions[i][1][0]][self.positions[i][1][1]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
            self.screen.blit(self.semafory[self.positions[i][1][2]][self.positions[i][1][3]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
        self.draw2()
        self.drawMouse()
        pygame.display.flip()

    def draw2(self):
        for i in range(len(self.positions)):
            if self.positions[i][1][0] == 3:
                self.screen.blit(self.squares[self.positions[i][1][0]][self.positions[i][1][1]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))

        self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"squares"+".png"),(0,0))
        if self.picked == 0: self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"selectedSquare"+".png"),(151,8))
        elif self.picked == 1: self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"selectedSquare"+".png"),(151,56))
        else: self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"selectedSquare"+".png"),(151,104))
        self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"transp"+".png"),(153,10))
        self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"transp"+".png"),(153,58))
        self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"transp"+".png"),(153,106))
        if self.selectedSquare%len(self.squares) == 3:
            self.screen.blit(self.squares[1][self.rotation%len(self.squares[self.selectedSquare%len(self.squares)])],(153,10))
        self.screen.blit(self.squares[self.selectedSquare%len(self.squares)][self.rotation%len(self.squares[self.selectedSquare%len(self.squares)])],(153,10))
        self.screen.blit(self.semafory2[self.selectedSquare%len(self.semafory2)],(153,58))
        self.screen.blit(self.dekorace[self.selectedSquare%len(self.dekorace)][self.rotation%len(self.dekorace[self.selectedSquare%len(self.dekorace)])],(153,106))
        
    def draw3(self):
        for i in range(len(self.trains)):
            self.screen.blit(self.trainImages[0][1],(self.trains[i][0]*self.textureSize+200,self.trains[i][1]*self.textureSize))
 
        for i in range(len(self.positions)):
            if self.positions[i][1][0] == 3:
                self.screen.blit(self.squares[self.positions[i][1][0]][self.positions[i][1][1]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
                
        self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"trainsSelect"+".png"),(0,0))
        if self.pickedTrain == 0: self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"selectTrain"+".png"),(123,18))
        elif self.pickedTrain == 1: self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"selectTrain"+".png"),(123,78))
        
        self.screen.blit(self.trainImages[self.selectedTrain%len(self.trainImages)][0],(125,20))
        self.screen.blit(self.trainImages[self.selectedTrain%len(self.trainImages)][0],(125,80))
        

    def drawMouse(self):
        self.mousePosition = pygame.mouse.get_pos()
        if self.mousePosition[0] > 200 or self.mousePosition[1] > 148:
            self.clickedSquare = (int(((self.mousePosition[0] - 200 - self.offset[0]*self.textureSize) - (self.mousePosition[0] -200 - self.offset[0]*self.textureSize)%self.textureSize)/self.textureSize)+self.offset[0], int((self.mousePosition[1] - self.offset[1]*self.textureSize - (self.mousePosition[1] - self.offset[1]*self.textureSize)%self.textureSize)/self.textureSize) + self.offset[1])
            
            self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"mouse"+".png"),(self.clickedSquare[0]*self.textureSize+200,self.clickedSquare[1]*self.textureSize))
            
    def simulaceDraw(self):
        self.screen.fill((0,0,0))
        for i in range(len(self.positions)):
            self.screen.blit(self.dekorace[self.positions[i][1][4]][self.positions[i][1][5]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
            if self.positions[i][1][0] == 3:
                self.screen.blit(self.squares[1][self.positions[i][1][1]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
            self.screen.blit(self.squares[self.positions[i][1][0]][self.positions[i][1][1]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
            self.screen.blit(self.semafory[self.positions[i][1][2]][self.positions[i][1][3]],((self.positions[i][0][0] + self.offset[0]) * self.textureSize + 200, (self.positions[i][0][1] + self.offset[1])*self.textureSize))
        self.draw3()
        self.drawMouse()
        pygame.display.flip()

    def startSimulation(self):
        self.Draw()
        self.screen.blit(pygame.image.load("textures/"+self.settings[1]+"/"+"askForSim"+".png"),((self.velikostX-300)/2,(self.velikostY-200)/2))
        pygame.display.flip()
        exit = True
        
        while exit == True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        exit = False
                        self.runSimulation()
                    elif event.key == K_n or event.key == K_ESCAPE:
                        exit = False
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] > (self.velikostX-300)/2+27 and pygame.mouse.get_pos()[1] > (self.velikostY-200)/2+135 and pygame.mouse.get_pos()[0] < (self.velikostX-300)/2+80 and pygame.mouse.get_pos()[1] < (self.velikostY-200)/2+188:
                        exit = False
                        self.runSimulation()
                    elif pygame.mouse.get_pos()[0] > (self.velikostX-300)/2+211 and pygame.mouse.get_pos()[1] > (self.velikostY-200)/2+135 and pygame.mouse.get_pos()[0] < (self.velikostX-300)/2+263 and pygame.mouse.get_pos()[1] < (self.velikostY-200)/2+188:
                        exit = False
                        
    def runSimulation(self):
        self.simulaceON = True
        self.makePaths.NewMap(self.positions)
        while self.simulaceON == True:
            self.GetInputs()
            self.MoveOnBoard()
            self.trains = self.makePaths.getPaths()
            self.simulaceDraw()
            time.sleep(1)
            
    def PlaceTrains(self):                    
        self.mousePosition = pygame.mouse.get_pos()
        if self.mousePosition[0] > 200 or self.mousePosition[1] > 148:
            self.clickedSquare = (int(((self.mousePosition[0] - 200 - self.offset[0]*self.textureSize) - (self.mousePosition[0] -200 - self.offset[0]*self.textureSize)%self.textureSize)/self.textureSize), int((self.mousePosition[1] - self.offset[1]*self.textureSize - (self.mousePosition[1] - self.offset[1]*self.textureSize)%self.textureSize)/self.textureSize))
            
            pos = [self.clickedSquare,0]
            clicked = 0
            while clicked == 0:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        clicked = 1

            self.mousePosition = pygame.mouse.get_pos()
            if self.mousePosition[0] > 200 or self.mousePosition[1] > 148:
                self.clickedSquare = (int(((self.mousePosition[0] - 200 - self.offset[0]*self.textureSize) - (self.mousePosition[0] -200 - self.offset[0]*self.textureSize)%self.textureSize)/self.textureSize), int((self.mousePosition[1] - self.offset[1]*self.textureSize - (self.mousePosition[1] - self.offset[1]*self.textureSize)%self.textureSize)/self.textureSize))
            
                pos[1] = self.clickedSquare
                
                self.makePaths.addtrain(pos,self.selectedTrain)
                

                        
    def GetInputs(self):
        for event in pygame.event.get():
            if event.type == QUIT: 
                self.running = False
                self.simulaceON = False
            elif event.type == VIDEORESIZE: 
                self.CorrectWindowSize(event)
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.pressedUP = True
                elif event.key == K_DOWN:
                    self.pressedDOWN = True
                elif event.key == K_LEFT:
                    self.pressedLEFT = True
                elif event.key == K_RIGHT:
                    self.pressedRIGHT = True
                    
                if event.key == K_LCTRL:
                    self.ctrl = True
                    
                if self.simulaceON == False:
                    if event.key == K_e:
                        self.picked = 0
                    elif event.key == K_r:
                        self.picked = 1
                    elif event.key == K_t:
                        self.picked = 2
                    
                    if event.key == K_w:
                        self.selectSquare(1,0)
                    if event.key == K_s:
                        self.selectSquare(-1,0)
                    if event.key == K_a:
                        self.selectSquare(0,1)
                    if event.key == K_d:
                        self.selectSquare(0,-1)
                    
                    if event.key == K_p:
                        #self.startSimulation()
                        self.runSimulation()
                    if event.key == K_m:
                        self.askForSave()
                    if event.key == K_n:
                        self.askForLoad()
                
                if self.simulaceON == True:
                    if event.key == K_w:
                        self.selectedTrain += 1
                    if event.key == K_e:
                        self.pickedTrain = 0
                    elif event.key == K_r:
                        self.pickedTrain = 1
                    if event.key == K_p:
                        self.simulaceON = False
                        
                    
            if event.type == KEYUP:
                if event.key == K_UP:
                    self.pressedUP = False
                elif event.key == K_DOWN:
                    self.pressedDOWN = False
                elif event.key == K_LEFT:
                    self.pressedLEFT = False
                elif event.key == K_RIGHT:
                    self.pressedRIGHT = False
                    
                if event.key == K_LCTRL:
                    self.ctrl = False
                    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
                if self.simulaceON == False:
                    if event.button == 3:
                        self.selectSquare(1,0)
                    elif event.button == 4:
                        self.selectSquare(0,-1)
                    elif event.button == 5:
                       self.selectSquare(0,1)
                if self.simulaceON == True:
                    self.PlaceTrains()
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicked = False
                
    def Place(self):
        self.mousePosition = pygame.mouse.get_pos()
        if self.mousePosition[0] > 200 or self.mousePosition[1] > 148:
            self.clickedSquare = (int(((self.mousePosition[0] - 200 - self.offset[0]*self.textureSize) - (self.mousePosition[0] -200 - self.offset[0]*self.textureSize)%self.textureSize)/self.textureSize), int((self.mousePosition[1] - self.offset[1]*self.textureSize - (self.mousePosition[1] - self.offset[1]*self.textureSize)%self.textureSize)/self.textureSize))
            if (self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][0][0],self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][0][1]) == self.clickedSquare:
                if self.picked == 0:
                    if self.ctrl == True:
                        self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][0] = 0
                        self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][1] = 0
                    else:
                        self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][0] = self.selectedSquare%len(self.squares)
                        self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][1] = self.rotation%len(self.squares[self.selectedSquare%len(self.squares)])
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][2] = 0
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][3] = 0
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][4] = 0
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][5] = 0
                elif self.picked == 1:
                    self.placeSemafor()
                elif self.picked == 2:
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][4] = self.selectedSquare%len(self.dekorace)
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][5] = self.rotation%len(self.dekorace[self.selectedSquare%len(self.dekorace)])
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][0] = 0
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][1] = 0
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][2] = 0
                    self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][3] = 0
                    if self.selectedSquare%len(self.dekorace) == 2:
                        self.trees.append([self.clickedSquare[0],self.clickedSquare[1],self.rotation%len(self.dekorace[self.selectedSquare%len(self.dekorace)])])
                        
                        
    def placeSemafor(self):
        if self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][0] == 1:
            if self.selectedSquare%len(self.semafory) == 1:
                self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][2] = 1
                self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][3] = self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][1]*2 + self.rotation%(int(len(self.semafory[self.selectedSquare%len(self.semafory)])/2))
            elif self.selectedSquare%len(self.semafory) == 2:
                self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][2] = 2
                self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][3] = self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][1]
            elif self.selectedSquare%len(self.semafory) == 3:
                self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][2] = 3
                self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][3] = self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][1]*2 + self.rotation%(int(len(self.semafory[self.selectedSquare%len(self.semafory)])/2))
        elif self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][0] == 4:
            if self.selectedSquare%len(self.semafory) == 2:
                self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][2] = 2
                self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][3] = 2
        if self.selectedSquare%len(self.semafory) == 0:
            self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][2] = 0
            self.positions[self.itoxy[self.clickedSquare[0]][self.clickedSquare[1]]][1][3] = 0
            
    def MoveOnBoard(self):
        speed = self.settings[3]
        if self.pressedUP == True:
            self.offset[1] += speed
            if self.offset[1] > 1:
                self.offset[1] = 1

        if self.pressedDOWN == True:
            self.offset[1] -= speed
            if self.offset[1] < -self.settings[2][1] + self.velikostY/self.textureSize - 1:
                self.offset[1] = -self.settings[2][1] + self.velikostY/self.textureSize - 1

        if self.pressedLEFT == True:
            self.offset[0] += speed
            if self.offset[0] > 0:
                self.offset[0] = 0
        if self.pressedRIGHT == True:
            self.offset[0] -= speed
            if self.offset[0] < -self.settings[2][0] + (self.velikostX-200)/self.textureSize - 1:
                self.offset[0] = -self.settings[2][0] + (self.velikostX-200)/self.textureSize - 1
                
    def selectSquare(self,a,b):
        self.selectedSquare -= b
        self.rotation += a
        
        if self.selectedSquare < 0:
            self.selectedSquare = 0
        if self.rotation < 0:
            self.rotation = 0
                
                
    def CreateBoard(self):
        sizeX = self.settings[2][0]
        sizeY = self.settings[2][1]        
        self.positions = []
        self.trees = []
        self.itoxy = []
        self.trains = []
        
        for x in range(sizeX):
            self.itoxy.append([])
            for y in range(sizeY):
                self.positions.append([[x,y],[0,0,0,0,0,0]]) #[[x,y],[blok,rotace,semafor,rotace,dekorace,rotace]]
                self.itoxy[-1].append(len(self.positions)-1)
                
                if random.randint(1,5) == 1 and self.settings[4] == "True":
                    self.positions[-1][1] = [0,0,0,0,1,random.randint(0,3)]
                    
                elif random.randint(1,15) == 1 and self.settings[5] == "True":
                    a = random.randint(0,4)
                    self.trees.append([x,y,a])
                    self.positions[-1][1] = [0,0,0,0,2,a]
                    
        if self.settings[5] == "True":
            self.growTrees()
                    
                    
    def growTrees(self):
        for i in range(len(self.trees)):
            if random.randint(1,500) == 1 and self.trees[i][2] < 4:
                self.trees[i][2] += 1
                
        for i in range(random.randint(0,5)):
            x = random.randint(0,self.settings[2][0]-1)
            y = random.randint(0,self.settings[2][1]-1)
            num = self.itoxy[x][y]
            if self.positions[num] == [[x,y],[0,0,0,0,0,0]]:
                self.trees.append([x,y,0])
        
        remove = []
        for i in range(len(self.trees)):
            if self.positions[self.itoxy[self.trees[i][0]][self.trees[i][1]]][1][:5] == [0,0,0,0,2]:
                self.positions[self.itoxy[self.trees[i][0]][self.trees[i][1]]][1] = [0,0,0,0,2,self.trees[i][2]]
            else:
                remove.append(i)
                
        for i in range(len(remove)):
            self.trees.pop(remove[i])
            for g in range(len(remove)):
                remove[g] -= 1
                
    def ReadSettings(self):
        f = open("settings.txt", "r")
        File = f.readlines()
        filE = [[int(File[0].split(":")[1][1:-1]), #msX
                 int(File[1].split(":")[1][1:-1]), #msY
                 int(File[2].split(":")[1][1:-1]), #MsX
                 int(File[3].split(":")[1][1:-1])], #MsY
                str(File[4].split(":")[1][1:-1]), #textures
                [int(File[5].split(":")[1][1:-1]), #sizeX
                 int(File[6].split(":")[1][1:-1])], #sizeY
                float(File[7].split(":")[1][1:-1]), #speedOfArrows
                str(File[8].split(":")[1][1:-1]), #grow Flowers
                str(File[9].split(":")[1][1:-1]) #grow Trees
                     ]
        if filE[0][2] > 2000:
            filE[0][2] = 2000
        if filE[0][3] > 2000:
            filE[0][3] = 2000
        return filE
    
    def CorrectWindowSize(self,event):
        width, height = event.size
        changed = False
        self.velikostX = width
        self.velikostY = height
        if width < self.settings[0][1]:
            width = self.settings[0][1]
            changed = True
        if height < self.settings[0][0]:
            height = self.settings[0][0]
            changed = True
        if height > self.settings[0][2]:
            height = self.settings[0][2]
            changed = True
        if width > self.settings[0][3]:
            width = self.settings[0][3]
            changed = True
            
        if changed == True:
            self.screen = pygame.display.set_mode((width,height), RESIZABLE)
            
    def LoadImages(self):
        self.textureSize = int(open("textures/"+self.settings[1]+"/textureSize.txt").readlines()[0])
        self.squares = []
        self.semafory = []
        self.dekorace = []
        self.semafory2 = []
        self.trainImages = []
        
        self.dekorace.append([])
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"grass"+".png"))
        
        self.dekorace.append([])
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"flower1"+".png"))
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"flower2"+".png"))
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"flower3"+".png"))
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"flower4"+".png"))
        
        self.dekorace.append([])
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"tree1"+".png"))
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"tree2"+".png"))
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"tree3"+".png"))
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"tree4"+".png"))
        self.dekorace[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"tree5"+".png"))
        
        self.squares.append([])
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"invis"+".png"))

        self.squares.append([])
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"straightRail1"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"straightRail2"+".png"))
        
        self.squares.append([])
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turn1"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turn2"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turn3"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turn4"+".png"))
        
        self.squares.append([])
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"station2"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"station1"+".png"))
        
        self.squares.append([])
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"crossroad"+".png"))
        
        self.squares.append([])
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turnout1"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turnout2"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turnout3"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turnout4"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turnout5"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turnout6"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turnout7"+".png"))
        self.squares[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"turnout8"+".png"))

        self.semafory.append([])
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"invis"+".png"))
        
        self.semafory.append([])
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor11"+".png"))
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor12"+".png"))
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor13"+".png"))
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor14"+".png"))
        self.semafory.append([])
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor21"+".png"))
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor22"+".png"))
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor41"+".png"))
        self.semafory.append([])
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor31"+".png"))
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor32"+".png"))
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor33"+".png"))
        self.semafory[-1].append(pygame.image.load("textures/"+self.settings[1]+"/"+"semafor34"+".png"))
        
        
        self.semafory2.append(pygame.image.load("textures/"+self.settings[1]+"/"+"invis"+".png"))
        self.semafory2.append(pygame.image.load("textures/"+self.settings[1]+"/"+"semaforSelect1"+".png"))
        self.semafory2.append(pygame.image.load("textures/"+self.settings[1]+"/"+"semaforSelect2"+".png"))
        self.semafory2.append(pygame.image.load("textures/"+self.settings[1]+"/"+"semaforSelect3"+".png"))
        
        image = self.getVehicleImages()
        for i in range(len(image)):
            if image[i][0] == 1:
                self.trainImages.append([])
                for g in range(12):
                    self.trainImages[-1].append(pygame.image.load("textures/"+self.settings[1]+"/trains/"+image[i][g+1]))
                    
        
        
        
    def getVehicleImages(self):
        l = open("textures/"+self.settings[1]+"/"+"trains.txt")
        images = []
        lines = l.readlines()
        for i in range(len(lines)):
            if lines[i][-1:] == "\n":
                lines[i] = lines[i][:-1]
                
        for i in range(len(lines)):
            if lines[i] == "-train":
                images.append([1])
                for g in range(12):
                    images[-1].append(lines[i+g+1])
                                        
        return images
                
mc = MainClass()






















