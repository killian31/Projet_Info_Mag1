import Globals
import math
import random
import Physics
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

def toss(x, y):
     flip = random.randint(0, 1)
     if flip == 0:
         return x
     else:
         return y

class Host(QtWidgets.QGraphicsItem):
    length = Globals.hostsLength
    width = 2*length/9
    bounds = QtCore.QRectF(-.5*length, -.5*width, length, width)
    
    def __init__(self, color, health, infected, x, y, a, timer, ID):
        super().__init__()
        self.color = color
        self.health = health
        self.infected = infected
        self.setPos(x, y) 
        self.setRotation(a)
        self.neighbors = []
        self.timer = timer
        self.ID = ID
        
    def move(self):
        a = self.rotation()
        p = Physics.t(self.pos())
        x, y = p
        a2 = math.pi*a/180
        xtemp = x + math.cos(a2)
        ytemp =  y + math.sin(a2)
        if self.inside(xtemp, ytemp):
            self.setPos(xtemp, ytemp)
            self.setRotation((a + random.uniform(-5, 5))%360)
        else:
            a_fin = (a + random.uniform(-5, 5)+90)%360
            self.setRotation(a_fin)
            x_fin = x + math.cos(a_fin)
            y_fin = y + math.sin(a_fin)
            self.setPos(x_fin, y_fin)

    def inside(self, x, y):
        size = Globals.environmentSize # 200
        extent = size/2

        if y > (extent):
            return False
        elif x > (extent):
            return False
        elif y < (-extent):
            return False
        elif x < (-extent):
            return False
        else:
            return True

    def paint(self, painter, option, widget=None): 
        painter.setPen(self.color)
        painter.drawRect(Host.bounds)
    
    def boundingRect(self):
        return Host.bounds
    
    def distance(self, B):
        x1, y1 = Physics.t(self.pos())
        x2, y2 = Physics.t(B.pos())
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def detection(self, physics) :
        self.neighbors = []
        p1 = Physics.t(self.pos())
        x1, y1 = p1
        for host in physics.hosts:
            if host != self : # you cant be your own neighbor
                p2 = Physics.t(host.pos())
                x2, y2 = p2
                if self.distance(host) ** 2 <= Globals.min_dist ** 2: # if you are in the circle you become a neighbor
                    self.neighbors.append(host)
                    
    def reproduction(self,physics):
        if len(physics.hosts) < Globals.MaxnbHosts and len(self.neighbors) > 0 and self.timer == 0:
            partner = random.choice(self.neighbors)
            proba_repro = 0.3
            P = random.uniform(0, 1)
            if P < proba_repro:
                x_partner, y_partner = Physics.t(partner.pos())
                x_self, y_self = Physics.t(self.pos())
                x_mean = (x_partner + x_self)/2
                y_mean = (y_partner + y_self) / 2
                physics.add_host(QtGui.QColor.fromRgbF(toss(self.color.redF(), partner.color.redF()),
                                                       toss(self.color.greenF(), partner.color.greenF()),
                                                       toss(self.color.blueF(),partner.color.blueF())),
                                                        1,
                                                        False,
                                                        x_mean, 
                                                        y_mean, 
                                                        random.uniform(0, 360), 500, 
                                                        len(physics.hosts) + 1)
               
                self.timer = 100
                for i, guy in enumerate(physics.hosts):
                    if guy.ID == partner.ID:
                        physics.hosts[i].timer = 100
                #partner.timer = 100

    def infection(self, physics):
        pass