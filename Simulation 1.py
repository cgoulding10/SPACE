import pygame
from pygame.locals import *
import sys
import math

pygame.init()
vec = pygame.math.Vector2

t = 0
FIRST = True
PLACE = 0
pi = 3.1416
r_e = 149.6 * (10**9)
r_m = 227.9 * (10**9)
HEIGHT = 800
WIDTH = 800
FPS = 120
G = 6.67430 * (10**(-11))
m3 = 1.989 * (10**30)
m2 = 5.97*(10**24)
m1 = 420000
SCALE = 50000
POINTS = [(400, 244)]
PERFRAME = 15
H = 10

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


class ISS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(400, 250))
        self.pos = vec(400,264)
        self.tra = False
        self.p1 = True
        self.p2 = True

    def initial(self, dir, dist, angle):
        speed = math.sqrt((G * m2) / dist) / SCALE
        if dir == 1:
            self.vel = vec(speed * math.sin(angle), -speed * math.cos(angle))
        if dir == 2:
            self.vel = vec(-speed * math.sin(angle), -speed * math.cos(angle))
        if dir == 3:
            self.vel = vec(-speed * math.sin(angle), speed * math.cos(angle))
        if dir == 4:
            self.vel = vec(speed * math.sin(angle), speed * math.cos(angle))
        if dir == 5:
            self.vel = vec(speed, 0)
        if dir == 6:
            self.vel = vec(-speed, 0)
        if dir == 7:
            self.vel = vec(0, speed)
        if dir == 8:
            self.vel = vec(0, -speed)

    def x(self):
        return (self.pos.x)
    def y(self):
        return (self.pos.y)
    def xv(self):
        return (self.vel.x)
    def yv(self):
        return (self.vel.y)
    def tra(self):
        return (self.tra)
    def fal(self):
        self.tra = False

    def calcpos(self,k1rx,k1ry,k2rx,k2ry,k3rx,k3ry,k4rx,k4ry):
        x = self.pos.x + (H/6)*(k1rx + 2*k2rx + 2*k3rx + k4rx)
        y = self.pos.y + (H/6)*(k1ry + 2*k2ry + 2*k3ry + k4ry)
        self.pos = vec(x,y)

    def calcvel(self, k1vx, k1vy, k2vx, k2vy, k3vx, k3vy, k4vx, k4vy):
        x = self.vel.x + (H / 6) * (k1vx + 2 * k2vx + 2 * k3vx + k4vx)
        y = self.vel.y + (H / 6) * (k1vy + 2 * k2vy + 2 * k3vy + k4vy)
        self.vel = vec(x,y)

    def move(self):
        self.rect.midbottom = self.pos

    def deltav1(self,r1,angle,dir):
        v1 = math.sqrt((G*m3)/r_e)
        vpi = math.sqrt(2*G*m3*((r_m)/(r_e*(r_e + r_m))))
        speed = math.sqrt(2*(((G*m2)/r1)+(((vpi-v1)**2))/2))/SCALE
        print(vpi-v1)
        self.tra = True
        tempx = self.vel.x
        tempy = self.vel.y
        if dir == 1:
            self.vel = vec(speed * math.sin(angle), -speed * math.cos(angle))
        if dir == 2:
            self.vel = vec(-speed * math.sin(angle), -speed * math.cos(angle))
        if dir == 3:
            self.vel = vec(-speed * math.sin(angle), speed * math.cos(angle))
        if dir == 4:
            self.vel = vec(speed * math.sin(angle), speed * math.cos(angle))
        if dir == 5:
            self.vel = vec(speed, 0)
        if dir == 6:
            self.vel = vec(-speed, 0)
        if dir == 7:
            self.vel = vec(0, speed)
        if dir == 8:
            self.vel = vec(0, -speed)

        if self.p1 == True:
            initial = math.sqrt((tempx**2)+(tempy**2))
            final = math.sqrt((self.vel.x**2)+(self.vel.y**2))
            print("Delta-v1: ",(final-initial)*SCALE,"m/s")
            print("Delta-v1: ", (final) * SCALE, "m/s")
            self.p1 = False



class EARTH(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill((0, 255, 255))
        self.rect = self.surf.get_rect(center=(400, 380))

        self.pos = vec(400, 400)
        self.vel = vec(0,0)
        self.acc = vec(0, 0)

    def x(self):
        return (self.pos.x)
    def y(self):
        return (self.pos.y)

def dist(x1,y1,x2,y2):
    r =  ((((x2-x1)*SCALE)**2)+(((y2-y1)*SCALE)**2)) ** 0.5
    return r

def acc(m,a,b,r):
    return (G*m*((a-b))/(r**3))

def draw(points):
    pygame.draw.lines(displaysurface,(255,255,255),False,points,3)

def angle(x1,y1,x2,y2,dir):
    if dir == 1 or dir == 2 or dir == 3 or dir == 4:
        return (math.atan(abs(y2-y1)/abs(x2-x1)))
    else:
        return 0

def period(r1,r2):
    a = (r1+r2)/2
    return math.sqrt((4*(math.pi**2)*(a**3))/(G*m2))/(H)

def dire(x1,y1,x2,y2):
    if x1-x2 > 0 and y1-y2 > 0 :
        return 1
    if x1-x2 > 0 and y1-y2 < 0:
        return 2
    if x1-x2 < 0 and y1-y2 < 0:
        return 3
    if x1-x2 < 0 and y1-y2 > 0:
        return 4
    if x1-x2 == 0 and y1-y2 > 0:
        return 5
    if x1-x2 == 0 and y1-y2 < 0:
        return 6
    if x1-x2 > 0 and y1-y2 == 0:
        return 7
    if x1-x2 < 0 and y1-y2 == 0:
        return 8

def eangle(r1,angle,dir):
    v1 = math.sqrt((G * m3) / r_e)
    vpi = math.sqrt(2*G * m3 * ((r_m) / (r_e * (r_e + r_m))))
    e = 1 + ((r1 * (vpi-v1)**2)/(G*m2))
    d = (math.asin(1/e))
    if dir == 1:
        if angle < d + 0.004 and angle > d - 0.004 :
            return True
        else:
            return False
    else:
        return False


P1 = ISS()
P2 = EARTH()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(P2)

P1.initial(dire(P1.x(),P1.y(),P2.x(),P2.y()),dist(P1.x(),P1.y(),P2.x(),P2.y()),
           angle(P1.x(),P1.y(),P2.x(),P2.y(),dire(P1.x(),P1.y(),P2.x(),P2.y())))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    displaysurface.fill((0, 0, 0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    POINTS.append((P1.x(), P1.y() - 20))
    draw(POINTS)

    k1vx = acc(m2,P2.x(),P1.x(),dist(P1.x(),P1.y(),P2.x(),P2.y()))
    k1vy = acc(m2,P2.y(),P1.y(),dist(P1.x(),P1.y(),P2.x(),P2.y()))
    k1rx = P1.xv()
    k1ry = P1.yv()

    k2vx = acc(m2,P2.x(),P1.x()+(H/2)*k1rx,dist(P1.x()+(H/2)*k1rx,P1.y()+(H/2)*k1ry,P2.x(),P2.y()))
    k2vy = acc(m2,P2.y(),P1.y()+(H/2)*k1ry,dist(P1.x()+(H/2)*k1rx,P1.y()+(H/2)*k1ry,P2.x(),P2.y()))
    k2rx = k1rx + (H/2)*k1vx
    k2ry = k1ry + (H/2)*k1vy

    k3vx = acc(m2,P2.x(),P1.x()+(H/2)*k2rx,dist(P1.x()+(H/2)*k2rx,P1.y()+(H/2)*k2ry,P2.x(),P2.y()))
    k3vy = acc(m2,P2.y(),P1.y()+(H/2)*k2ry,dist(P1.x()+(H/2)*k2rx,P1.y()+(H/2)*k2ry,P2.x(),P2.y()))
    k3rx = k1rx + (H/2)*k2vx
    k3ry = k1ry + (H/2)*k2vy

    k4vx = acc(m2,P2.x(),P1.x()+(H)*k3rx,dist(P1.x()+(H)*k3rx,P1.y()+(H)*k3ry,P2.x(),P2.y()))
    k4vy = acc(m2,P2.y(),P1.y()+(H)*k3ry,dist(P1.x()+(H)*k3rx,P1.y()+(H)*k3ry,P2.x(),P2.y()))
    k4rx = k1rx + (H)*k3vx
    k4ry = k1ry + (H)*k3vy

    P1.calcpos(k1rx,k1ry,k2rx,k2ry,k3rx,k3ry,k4rx,k4ry)
    P1.calcvel(k1vx,k1vy,k2vx,k2vy,k3vx,k3vy,k4vx,k4vy)

    if (eangle(dist(P1.x(), P1.y(), P2.x(), P2.y()),
               angle(P1.x(), P1.y(), P2.x(), P2.y(), dire(P1.x(), P1.y(), P2.x(), P2.y())),
               dire(P1.x(), P1.y(), P2.x(), P2.y())) == True) and FIRST == True:
        PLACE = PLACE + 1
        if PLACE == 2:
            P1.deltav1(dist(P1.x(), P1.y(), P2.x(), P2.y()),
                       angle(P1.x(), P1.y(), P2.x(), P2.y(), dire(P1.x(), P1.y(), P2.x(), P2.y())),
                       dire(P1.x(), P1.y(), P2.x(), P2.y()))
            print(angle(P1.x(), P1.y(), P2.x(), P2.y(), dire(P1.x(), P1.y(), P2.x(), P2.y()))*(180/math.pi))

    P1.move()
    pygame.display.update()
    FramePerSec.tick(FPS)