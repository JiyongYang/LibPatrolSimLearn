import random
import os

from math import *
from Parser import *
from Drawer import *

class Calculator:
    def __init__(self, mapSizeX, mapSizeY, sizeOfGrid):
        self.recentPtLst = list()
        self.cumulatedPolicyHeatmap = np.zeros((101, 101, 8), dtype='f')
        self.checkNumber = 5
        self.mapSizeX = mapSizeX
        self.mapSizeY = mapSizeY
        self.sizeOfGrid = sizeOfGrid
        self.ratio_w = mapSizeX / sizeOfGrid
        self.ratio_h = mapSizeY / sizeOfGrid

    def setCheckNumber(self, n):
        self.checkNumber = n

    def calCumulatePolicyHeatmap(self, policyHeatmap):
        for i in range(len(policyHeatmap)):
            for j in range(len(policyHeatmap[i])):
                for k in range(len(policyHeatmap[i][j])):
                    self.cumulatedPolicyHeatmap[i][j][k] += policyHeatmap[i][j][k]

    def getPolicyHeatmap(self):
        return self.cumulatedPolicyHeatmap

    def initial_learn(self, fileName):
        lst = ReadXML(fileName, self.mapSizeX, self.mapSizeY, self.sizeOfGrid)
        for agent in lst:
            agent.calHoG()
            agent.calHeatmap()
            agent.calPolicyHeatmap()
            self.calCumulatePolicyHeatmap(agent.getPolicyHeatmap())

    def learn(self, fileName):
        lst = ReadXML(fileName, self.mapSizeX, self.mapSizeY, self.sizeOfGrid)
        self.loadData()
        for agent in lst:
            agent.calHoG()
            agent.calHeatmap()
            agent.calPolicyHeatmap()
            self.calCumulatePolicyHeatmap(agent.getPolicyHeatmap())

    def saveData(self):
        if not os.path.exists('learnedData'):
            os.makedirs('learnedData')

        np.savetxt('learnedData/ld_right.txt', cal.getPolicyHeatmap()[:, :, 0], fmt = '%0.1f')
        np.savetxt('learnedData/ld_rightup.txt', cal.getPolicyHeatmap()[:, :, 1], fmt = '%0.1f')
        np.savetxt('learnedData/ld_up.txt', cal.getPolicyHeatmap()[:, :, 2], fmt = '%0.1f')
        np.savetxt('learnedData/ld_leftup.txt', cal.getPolicyHeatmap()[:, :, 3], fmt = '%0.1f')
        np.savetxt('learnedData/ld_left.txt', cal.getPolicyHeatmap()[:, :, 4], fmt = '%0.1f')
        np.savetxt('learnedData/ld_leftdown.txt', cal.getPolicyHeatmap()[:, :, 5], fmt = '%0.1f')
        np.savetxt('learnedData/ld_down.txt', cal.getPolicyHeatmap()[:, :, 6], fmt = '%0.1f')
        np.savetxt('learnedData/ld_rightdown.txt', cal.getPolicyHeatmap()[:, :, 7], fmt = '%0.1f')

    def loadData(self):
        filelist = ['ld_right.txt', 'ld_rightup.txt', 'ld_up.txt', 'ld_leftup.txt', 'ld_left.txt', 'ld_leftdown.txt', 'ld_down.txt', 'ld_rightdown.txt']
        cumulatedPolicyHeatmap = np.zeros((101, 101, 8), dtype='f')

        # folding array layer
        for i in range(8):
            cumulatedPolicyHeatmap[:,:,i] = np.loadtxt("learnedData/"+filelist[i])
        self.cumulatedPolicyHeatmap = cumulatedPolicyHeatmap

    def drawData(self):
        drawer = Drawer()
        drawer.render()
        drawer.print_value_all(self.cumulatedPolicyHeatmap)

    def calDir(self, angle):
        dir = None
        # right
        if (angle >= 337.5 or angle < 22.5):
            dir = 0
        # rightup
        elif (angle >= 22.5 and angle < 67.5):
            dir = 1
        # up
        elif (angle >= 67.5 and angle < 112.5):
            dir = 2
        # leftup
        elif (angle >= 112.5 and angle < 157.5):
            dir = 3
        # left
        elif (angle >= 157.5 and angle < 202.5):
            dir = 4
        # leftdown
        elif (angle >= 202.5 and angle < 247.5):
            dir = 5
        # down
        elif (angle >= 247.5 and angle < 292.5):
            dir = 6
        # rightdown
        elif (angle >= 292.5 and angle < 337.5):
            dir = 7

        return dir

    def checkWithFilter(self, cx, cy, _dir):
        # 9 by 9 filter
        filter = [(-1,-1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

        tendency = 0
        for fPt in filter:
            x = cx + fPt[0]
            y = cy + fPt[1]
            if x > 0 and x < (self.mapSizeX-1) and y > 0 and y < (self.mapSizeY-1):
                temp = 0
                tdir = 0
                for i in range(8):
                    val = self.cumulatedPolicyHeatmap[x][y][i]
                    if val > temp:
                        temp = val
                        tdir = i
                if temp != 0:
                    if _dir == tdir:
                        tendency += 1
        if tendency >= 1:
            return "Normal"
        else:
            return "Abnormal"

    def check(self, point):
        # check number of points
        if len(self.recentPtLst) >= self.checkNumber:
            lst = self.recentPtLst
            # processing
            post_pt = None
            for pt in lst:
                if post_pt != None:
                    px, py, pz = post_pt
                    cx, cy, cz = pt

                    dx = (cx - px)
                    dy = (cy - py)

                    angle = atan2(dy, dx) * 180 / pi

                    if angle < 0:
                        angle += 360

                    dir = self.calDir(angle)

                    cellpos_x = int(px / self.ratio_w)
                    cellpos_y = int(py / self.ratio_h)

                    result = checkWithFilter(cellpos_x, cellpos_y, dir)
                    print(result)
                post_pt = pt
            # delete oldest data
            tLst = lst[1:]
            self.recentPtLst = tlst
            print(self.recentPtLst)
        else:
            self.recentPtLst.append(point)


    def checkWithPoints(self, ptLst):
        self.loadData()
        post_pt = None
        for pt in ptLst:
            if post_pt != None:
                px, py, pz = post_pt
                cx, cy, cz = pt

                dx = (cx - px)
                dy = (cy - py)

                angle = atan2(dy, dx) * 180 / pi

                if angle < 0:
                    angle += 360

                dir = self.calDir(angle)

                cellpos_x = int(px / self.ratio_w)
                cellpos_y = int(py / self.ratio_h)

                result = self.checkWithFilter(cellpos_x, cellpos_y, dir)
                print(result)
            post_pt = pt





if __name__ == "__main__":
    #initial_learn("training2/training.xml")
    #load_learnedData()
    mapSizeX = 101
    mapSizeY = 101
    sizeOfGrid = 101
    cal = Calculator(mapSizeX, mapSizeY, sizeOfGrid)
    #cal.initial_learn("training2/training.xml")
    #cal.learn("training2/training.xml")
    #cal.saveData()

    #cal.drawData()

    cal.checkWithPoints([(86,74.125,0), (85,75.125,0), (84,76.125,0), (73,75.125,0), (82,36.125,0)])




"""
def initial_learn(fileName):
    lst = ReadXML(fileName)

    cal = Calculator()

    for agent in lst:
        agent.calHoG()
        agent.calHeatmap()
        agent.calPolicyHeatmap()
        cal.cumulatePolicyHeatmap(agent.getPolicyHeatmap())
        #plt.imshow(agent.getHog(), cmap='hot', interpolation='nearest')
        #plt.show()

    #drawer = Drawer()
    #drawer.render()
    #drawer.print_value_all(cal.getPolicyHeatmap())

    np.savetxt('learnedData/ld_right.txt', cal.getPolicyHeatmap()[:, :, 0], fmt = '%0.1f')
    np.savetxt('learnedData/ld_rightup.txt', cal.getPolicyHeatmap()[:, :, 1], fmt = '%0.1f')
    np.savetxt('learnedData/ld_up.txt', cal.getPolicyHeatmap()[:, :, 2], fmt = '%0.1f')
    np.savetxt('learnedData/ld_leftup.txt', cal.getPolicyHeatmap()[:, :, 3], fmt = '%0.1f')
    np.savetxt('learnedData/ld_left.txt', cal.getPolicyHeatmap()[:, :, 4], fmt = '%0.1f')
    np.savetxt('learnedData/ld_leftdown.txt', cal.getPolicyHeatmap()[:, :, 5], fmt = '%0.1f')
    np.savetxt('learnedData/ld_down.txt', cal.getPolicyHeatmap()[:, :, 6], fmt = '%0.1f')
    np.savetxt('learnedData/ld_rightdown.txt', cal.getPolicyHeatmap()[:, :, 7], fmt = '%0.1f')

def load_learnedData():
    # load data
    filelist = ['ld_right.txt', 'ld_rightup.txt', 'ld_up.txt', 'ld_leftup.txt', 'ld_left.txt', 'ld_leftdown.txt', 'ld_down.txt', 'ld_rightdown.txt']
    cumulatedPolicyHeatmap = np.zeros((101, 101, 8), dtype='f')

    # folding array layer
    for i in range(8):
        cumulatedPolicyHeatmap[:,:,i] = np.loadtxt("learnedData/"+filelist[i])

    # draw
    drawer = Drawer()
    drawer.render()
    drawer.print_value_all(cumulatedPolicyHeatmap)

"""
