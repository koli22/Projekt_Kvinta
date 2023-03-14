from copy import deepcopy

class MakePaths:
    def __init__(self):
        self.LoadRailsMap()
        self.Paths = []
        self.phase = 0
        self.trains = []
        
        #NEW VERSION
        self.trainPaths = []
        
    def NewMap(self,blocks):
        self.rails = []
        self.semafors = []
        self.paths = []
        self.railsXY = []

        x = 0
        y = 0
        for i in range(len(blocks)):
            if blocks[i][0][0] > x:
                x = blocks[i][0][0]
            if blocks[i][0][1] > y:
                y = blocks[i][0][1]
                
        x += 1
        y += 1
                
        self.rails = []
        self.semafors = []
        self.paths = []
        for i in range(x):
            self.rails.append([])
            self.semafors.append([])
            for g in range(y):
                self.rails[-1].append([0,0])
                self.semafors[-1].append([0,0])
                
        for i in range(len(blocks)):
            self.semafors[blocks[i][0][0]][blocks[i][0][1]] = [blocks[i][1][2],blocks[i][1][3]]
            self.rails[blocks[i][0][0]][blocks[i][0][1]] = [blocks[i][1][0],blocks[i][1][1]]
        
        for x in range(len(self.rails)):
            self.railsXY.append([])
            for y in range(len(self.rails[0])):
                self.railsXY[-1].append([])
                
                for i in range(len(self.railsMap)):
                    if self.railsMap[i][0] == self.rails[x][y][0]:
                        self.railsXY[x][y] = deepcopy(self.railsMap[i][1][self.rails[x][y][1]])
                        
                        
        for x in range(len(self.rails)):
            for y in range(len(self.rails[-1])):
                for i in range(len(self.railsXY[x][y])):
                    for g in range(len(self.railsXY[x][y][i])):
                        self.railsXY[x][y][i][g][0] += x
                        self.railsXY[x][y][i][g][1] += y
                self.railsXY[x][y] = [deepcopy(self.semafors[x][y]),deepcopy(self.railsXY[x][y])]
                    
        self.MakePaths()
                        
    
    def LoadRailsMap(self):
        self.railsMap = []
        lines = open("OtherScripts/rails.txt").readlines()
        for i in range(len(lines)):
            if lines[i][-1:] == "\n":
                lines[i] = lines[i][:-1]
            line = lines[i].split("/")
            try: 
                self.railsMap.append([int(line[0]),[]])
                do = 0
            except:
                do = 1
            if do == 0:
                line = line[1].split("-")
                for g in range(len(line)):
                    self.railsMap[-1][1].append([])
                    for k in range(len(line[g].split(","))):
                        self.railsMap[-1][1][-1].append(line[g].split(",")[k][1:-1].split(" "))
                        self.railsMap[-1][1][-1][-1][0] = int(self.railsMap[-1][1][-1][-1][0])
                        self.railsMap[-1][1][-1][-1][1] = int(self.railsMap[-1][1][-1][-1][1])
                                                
        for i in range(len(self.railsMap)):
            for g in range(len(self.railsMap[i][1])):
                for k in range(len(self.railsMap[i][1][g])):
                    for l in range(2):
                        if self.railsMap[i][1][g][k][l] == 0:
                            self.railsMap[i][1][g][k][l] = [0,-1]
                        elif self.railsMap[i][1][g][k][l] == 1:
                            self.railsMap[i][1][g][k][l] = [-1,0]
                        elif self.railsMap[i][1][g][k][l] == 2:
                            self.railsMap[i][1][g][k][l] = [0,1]
                        elif self.railsMap[i][1][g][k][l] == 3:
                            self.railsMap[i][1][g][k][l] = [1,0]
                            
                            
    def MakePaths(self):
        self.startingPoints = []
        
        for x in range(len(self.railsXY)):
            for y in range(len(self.railsXY[x])):
                if self.railsXY[x][y][0][0] != 0:
                    self.startingPoints.append([x,y])
                if self.rails[x][y][0] == 3:
                    self.railsXY[x][y][0][0] = 4
                    self.railsXY[x][y][0][1] = self.rails[x][y][1]
                    self.startingPoints.append([x,y])
                    
        for i in range(len(self.startingPoints)):
            paths = [[self.startingPoints[i],[0,0],[self.startingPoints[i]]]]
            for g in range(len(self.railsXY[self.startingPoints[i][0]][self.startingPoints[i][1]][1])):
                    paths.append(deepcopy(paths[0]))
                    paths[-1][1] = deepcopy(self.railsXY[self.startingPoints[i][0]][self.startingPoints[i][1]][1][g][0])
                    
            paths.pop(0)
            
            for path in paths:
                path[2].append(path[1])
                prom = self.railsXY[path[2][-1][0]][path[2][-1][1]]
                if prom[0][0] != 0:
                    self.paths.append(deepcopy(path))
                    path[1] = [-1,-1]
                elif prom[1] == []:
                    path[1] = [-1,-1]
                else:
                    for h in range(len(prom[1])):
                        if prom[1][h][0] == path[2][-2]:
                            paths.append(deepcopy(path))
                            paths[-1][1] = deepcopy(prom[1][h][1])
                            if paths[-1][2].count(paths[-1][1]) > 0 and self.rails[paths[-1][1][0]][paths[-1][1][1]][0] != 4:
                                paths[-1][1] = [-1,-1]
                            
                    path[1] = [-1,-1]
                    
            h = 0
            while h < len(paths):
                if paths[h][1] == [-1,-1]:
                    paths.pop(h)
                else:
                    h+=1
                    
        
    #zacatek bolesti
    def addtrain(self,pos,Type):
        #prida vlak
        pass
            
    def getPaths(self):
        #da pozice vlaku
        ret = []
        for path in self.paths:
            ret.append(path[-1][-1])
            
        return ret
            
                    
                    
                    
                    
                
                
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
        
