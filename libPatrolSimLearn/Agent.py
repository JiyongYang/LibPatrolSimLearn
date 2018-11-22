import numpy as np
from math import *

class Agent(object):
    def __init__(self, id, sc, name, type, spd, mapSizeX, mapSizeY, sizeOfGrid = 101):
        # Agent basic info
        self.id = id
        self.name = name
        self.type = type
        self.spd = spd
        self.sc = sc
        self.wayPoints = list()
        self.mapSizeX = mapSizeX
        self.mapSizeY = mapSizeY

        # Env info
        self.sizeOfGrid = sizeOfGrid
        self.ratio_w = mapSizeX / sizeOfGrid
        self.ratio_h = mapSizeY / sizeOfGrid

        # Strategy of agent
        # occurrence
        self.heatmap = np.zeros((sizeOfGrid, sizeOfGrid), dtype="i")
        # direction
        self.hog = np.full((sizeOfGrid, sizeOfGrid), -1)
        # policy heatmap
        # 0 : right / 1 : rightup / 2 : up / 3 : leftup
        # 4 : left / 5 : leftdown / 6 : down / 7 : rightdown
        self.policyHeatmap = np.zeros((sizeOfGrid, sizeOfGrid, 8), dtype="f")

    def __str__(self):
        return "|---- [[Agent Info]] ----|\n"\
        "|@Id : {}\t\t |\n|@Name : {}\t\t |\n|@Type : {}\t\t |\n|@Speed : {}\t\t |\n"\
        "|------------------------|".format(self.id, self.name, self.type, self.spd)

    def addWayPoint(self, point):
        self.wayPoints.append(point)

    def getWayPointList(self):
        return self.wayPoints

    def _setHeatmap(self, hm):
        self.heatmap = hm

    def getHeatmap(self):
        return self.heatmap

    def _setHog(self, hog):
        self.hog = hog

    def getHog(self):
        return self.hog

    def getPolicyHeatmap(self):
        return self.policyHeatmap

    def calHeatmap(self):
        for pt in self.wayPoints:
            x, y, z = pt.getPoint()
            self.updateHeatmap(x, y)

    def angle_between(self, p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return np.rad2deg((ang1 - ang2) % (2 * np.pi))

    def updateHeatmap(self, x, y):
        cellpos_x = int(x / self.ratio_w)
        cellpos_y = int(y / self.ratio_h)
        self.heatmap[cellpos_x][cellpos_y] += 1

    def calHoG(self):
        post_pt = None
        for pt in self.wayPoints:
            if post_pt != None:
                px, py, pz = post_pt
                cx, cy, cz = pt.getPoint()
                #print(post:',px, py,' || cur:',cx, cy)

                dx = (cx - px)
                dy = (cy - py)

                angle = atan2(dy, dx) * 180 / pi

                if angle < 0:
                    angle += 360

                cellpos_x = int(px / self.ratio_w)
                cellpos_y = int(py / self.ratio_h)
                self.hog[cellpos_x][cellpos_y] = angle
            post_pt = pt.getPoint()

    def calPolicyHeatmap(self):
        for pt in self.wayPoints:
            cx, cy, cz = pt.getPoint()

            cellpos_cx = int(cx / self.ratio_w)
            cellpos_cy = int(cy / self.ratio_h)

            angle = self.hog[cellpos_cx][cellpos_cy]

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

            for i in range(8):
                if dir == i:
                    self.policyHeatmap[cellpos_cx][cellpos_cy][i] += 1
                else:
                    #print("=" + str(cellpos_cx) + ","+ str(cellpos_cy) + "," + str(i))
                    #print(self.policyHeatmap[cellpos_cx][cellpos_cy][i])
                    self.policyHeatmap[cellpos_cx][cellpos_cy][i] -= 0.3
                    #print(self.policyHeatmap[cellpos_cx][cellpos_cy][i])

class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def getPoint(self):
        return (self.x, self.y, self.z)

    def setPoint(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
