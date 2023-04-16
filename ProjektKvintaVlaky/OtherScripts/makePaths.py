from copy import deepcopy
from OtherScripts.Algorithm import main
import time

class MakePaths:
    def __init__(self):
        self.LoadRailsMap()
        self.Paths = []
        self.phase = 0
        self.trains = []
        self.calculator = main()
        self.calculatedPaths = []
        
        #NEW VERSION (is fucked up)
        self.trainPaths = []
        self.trainsadded = []
        self.move = 0
        self.orders = []
        self.lastTime = 0
        
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
                    
        epoints = []
        for path in self.paths:
            if epoints.count(str(path[0][0]) + "," + str(path[0][1])) == 0:
                epoints.append(str(path[0][0]) + "," + str(path[0][1]))
                
            if epoints.count(str(path[1][0]) + "," + str(path[1][1])) == 0:
                epoints.append(str(path[1][0]) + "," + str(path[1][1]))
                    
        self.calculator.Points(epoints)
        paths = []
        for path in self.paths:
            paths.append((str(path[0][0]) + "," + str(path[0][1]), str(path[1][0]) + "," + str(path[1][1]), len(path[2])))
            
        self.calculator.Paths(paths)
                    
        
    #zacatek bolesti
    
    def GetPathsForTrains(self):
        trains = []
        for i in range(len(self.trainsadded)):
            trains.append((str(self.trainsadded[i][0][0]) + "," + str(self.trainsadded[i][0][1]) ,str(self.trainsadded[i][1][0]) + "," + str(self.trainsadded[i][1][1])))
            
            
        for train in self.trainsadded:
            end = train[0]
            train[0] = train[1]
            train[1] = end
            
        return self.calculator.Calculate(trains)
    
    def createOrders(self):
        self.lastTime = 0
        self.move = -1
        paths = self.GetPathsForTrains()
        orders = []
        
        for path in paths:
            
            if path == None:
                continue
            
            order = []
            longorder = []
            
            for g in range(len(path) - 1):
                for Path in self.paths:
                    if Path[0] == [int(path[0 + g].split(",")[0]),int(path[0 + g].split(",")[1])] and Path[1] == [int(path[1 + g].split(",")[0]),int(path[1 + g].split(",")[1])]:
                        order = deepcopy(Path[2])
                        
                for orde in order:
                    if len(longorder) > 0:
                        if longorder[-1] != orde:
                            longorder.append(deepcopy(orde))
                    else:
                        longorder.append(deepcopy(orde))
                    
            orders.append(deepcopy(longorder))
            
            
            startingRotation = self.getPossibleRotations(orders[-1][0], 0, 0, 0)[0];
            orders[-1][0] = [orders[-1][0][0] , orders[-1][0][1], startingRotation]
            
            prev = startingRotation
            
            _len = len(orders[-1]) - 2
        
        
            for i in range(len(orders[-1]) - 1):
                posRot1 = startingRotation - 1;
                posRot2 = startingRotation + 1;
            
                if posRot1 < 0:
                    posRot1+= 8;
            
                if posRot2 > 7:
                    posRot2 -= 8;
                    
                _next = orders[-1]
                _now = orders[-1]
                
                if i < _len:
                    _next = orders[-1][i + 2]
                    
                if i < _len + 1:
                    _now = orders[-1][i]
                
                rotations = self.getPossibleRotations(orders[-1][i + 1], prev, _next, _now)
                
                if len(rotations) == 4:
                    if rotations[0] == posRot1 or rotations[0] == posRot2:
                        startingRotation = rotations[0]
                        prev = rotations[2]
                    else:
                        startingRotation = rotations[1]
                        prev = rotations[3]
                    

                else:
                    if rotations[0] == startingRotation or rotations[1] == startingRotation:
                        pass
                    elif rotations[0] == posRot1 or rotations[0] == posRot2:
                        startingRotation = rotations[0]
                    else:
                        startingRotation = rotations[1]
                        
                    prev = startingRotation
                
                orders[-1][i + 1] = [orders[-1][i + 1][0] , orders[-1][i + 1][1], startingRotation]
            
        self.orders = orders
        
        
    def GetOrders(self):
        if (round(time.time()) != self.lastTime):
            if self.lastTime != 0:
                self.move += round(time.time()) - self.lastTime
                self.lastTime = round(time.time())
            else:
                self.move += 1
                self.lastTime = round(time.time())
                
        ret = []
        
        for order in self.orders:
            if len(order) < self.move + 1:
                ret.append(order[-1])
            else:
                ret.append(order[self.move])
                
                
        return ret
            
            
    
    
    
    def AddTrain(self,xy,gej):
        x = xy[0]
        y = xy[1]
        
        
        if self.has(self.trainsadded, x) != True and self.has(self.trainsadded, y) != True:
            self.trainsadded.append([x,y])
            
            self.orders.append([[x[0], x[1], self.getPossibleRotations(x, 0, 0, 0)[0]]])
    
    def RemoveTrain(self,x):
        if self.has(self.trainsadded, x) == True:
            self.trainsadded = self._del(self.trainsadded, x)

        
    def has(self,_list,x): 
        for i in range(len(_list)): 
            if _list[i][0] == x or _list[i][1] == x: 
                return True
        
    def _del(self,_list,x): 
        for i in _list: 
            if i[0] == x:
                _list.pop(i)
        return
    
    def Clear(self):
        self.orders = []
        
        
    def getPossibleRotations(self, position, prev, _next, _now):
        blok = self.rails[position[0]][position[1]]
        if blok[0] == 1 or blok[0] == 3:
            if blok[1] == 0:
                return [5, 1]
            elif blok[1] == 1:
                return [7, 3]
        if blok[0] == 4:
            if prev == 1 or prev == 5: 
                return [1,5]
            elif prev == 7 or prev == 3:
                return [3,7]
        if blok[0] == 2:
            if blok[1] == 0:
                if prev == 7 or prev == 3:
                    return [4, 8, 5, 1]
                else:
                    return [4, 8, 3, 7]  
                
            if blok[1] == 1:
                if prev == 7 or prev == 3:
                    return [6, 2, 1, 5]  
                else:
                    return [6, 2, 7, 3]  
            
            if blok[1] == 2:
                if prev == 3 or prev == 1:
                    return [4, 8, 5, 7]  
                else:
                    return [4, 8, 3, 1]  
            
            if blok[1] == 3:
                if prev == 1 or prev == 7:
                    return [2, 6, 7, 1]  
                else:
                    return [2, 6, 1, 7]  
            
        print(_now, _next)
        if blok[0] == 5 and _now[0] != _next[0] and _now[1] != _next[1]:
            print("tocna")
            if blok[1] == 0:
                if prev == 7 or prev == 3:
                    return [4, 8, 5, 1]
                else:
                    return [4, 8, 3, 7]  
                
            if blok[1] == 1:
                if prev == 7 or prev == 3:
                    return [6, 2, 1, 5]  
                else:
                    return [6, 2, 7, 3]  
            
            if blok[1] == 2:
                if prev == 3 or prev == 1:
                    return [4, 8, 5, 7]  
                else:
                    return [4, 8, 3, 1]  
            
            if blok[1] == 3:
                if prev == 1 or prev == 7:
                    return [2, 6, 7, 1]  
                else:
                    return [2, 6, 1, 7]  
        
        elif blok[0] == 5 and (_now[0] == _next[0] or _now[1] == _next[1]):
            if blok[1] == 0 or blok[1] == 1 or blok[1] == 2 or blok[1] == 3:
                return [5, 1]
            else:           
                return [7, 3]
            
        return [0,0]
    
    def ClearAll(self):
        self.trainsadded = []
        self.orders = []
    
    
    
         
            
                    
                      
                    
                    
                
                
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
        
