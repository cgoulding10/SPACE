import pygame
from pygame.locals import *
import sys
import math

pygame.init()
vec = pygame.math.Vector2

m_y = 5.9334 * (10**7)
h_t = 2.235 * (10**7)
m_o = 3.79 * (10**6)
pi = 3.1416
r_e = 149.6 * (10**9)
r_m = 227.9 * (10**9)
HEIGHT = 800
WIDTH = 800
FPS = 120
G = 6.67430 * (10**(-11))
m3 = 1.989 * (10**30)
m2 = 6.39 * (10**23)
m1 = 420000
SCALE = 625000000
v2 = math.sqrt((G * m3) / r_m)
vpi = math.sqrt(G * m3 * ((r_e) / (r_m * (r_e + r_m))))
vinf = v2 - vpi
H = 30000
EPOINTS = [(400,380 + (r_m)/SCALE)]
POINTS = [(400,380 + (r_e)/SCALE)]
PERFRAME = 15
TIMER = False
periodx = -1000
T = 0
ang = math.pi-((h_t/m_y) * 2 * math.pi)
FIRST = True

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


class ISS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(400, 250))
        self.pos = vec(400,400 + (r_e)/SCALE)
        self.tra = False
        self.p1 = True
        self.p2 = True

    def initial(self, dir, dist, angle):
        speed = math.sqrt((G * m3) / dist) / SCALE
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

    def deltav1(self,r1,r2,angle,dir):
        speed = math.sqrt(2*G*m3*(r2/(r1*(r1+r2))))/SCALE
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
            self.p1 = False

    def deltav2(self,r2,angle,dir):
        speed = math.sqrt((G*m3)/r2)/SCALE
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

        if self.p2 == True:
            initial = math.sqrt((tempx ** 2) + (tempy ** 2))
            final = math.sqrt((self.vel.x ** 2) + (self.vel.y ** 2))
            print("Delta-v2: ", (final - initial) * SCALE,"m/s")
            self.p2 = False



    def move(self):
        self.rect.midbottom = self.pos

class MARS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(400, 250))
        self.pos = vec(400,400 + (r_m)/SCALE)
        self.tra = False
        self.p1 = True
        self.p2 = True

    def initial(self, dir, dist, angle):
        speed = math.sqrt((G * m3) / dist) / SCALE
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

class SUN(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill((255, 100, 100))
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
    return math.sqrt((4*(math.pi**2)*(a**3))/(G*m3))/(H)

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

def cosrule(r1,r2,r3):
    return (math.acos(((r1**2)+(r2**2)-(r3**2))/(2*r1*r2)))

def eangle(a,dir1,dir2):
    if (dir1 > dir2 and dir1 <= 4 and dir2 <= 4) or (dir1 == 1 and dir2 == 4) :
        if a < ang and a != 0:
            if FIRST == True:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

P1 = ISS()
P2 = MARS()
P3 = SUN()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(P2)
all_sprites.add(P3)

P1.initial(dire(P1.x(),P1.y(),P3.x(),P3.y()),dist(P1.x(),P1.y(),P3.x(),P3.y()),
           angle(P1.x(),P1.y(),P3.x(),P3.y(),dire(P1.x(),P1.y(),P3.x(),P3.y())))

P2.initial(dire(P2.x(),P2.y(),P3.x(),P3.y()),dist(P2.x(),P2.y(),P3.x(),P3.y()),
           angle(P2.x(),P2.y(),P3.x(),P3.y(),dire(P2.x(),P2.y(),P3.x(),P3.y())))

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

    EPOINTS.append((P2.x(), P2.y() - 20))
    draw(EPOINTS)

    k1vx = acc(m3,P3.x(),P1.x(),dist(P1.x(),P1.y(),P3.x(),P3.y()))
    k1vy = acc(m3,P3.y(),P1.y(),dist(P1.x(),P1.y(),P3.x(),P3.y()))
    k1rx = P1.xv()
    k1ry = P1.yv()

    k2vx = acc(m3,P3.x(),P1.x()+(H/2)*k1rx,dist(P1.x()+(H/2)*k1rx,P1.y()+(H/2)*k1ry,P3.x(),P3.y()))
    k2vy = acc(m3,P3.y(),P1.y()+(H/2)*k1ry,dist(P1.x()+(H/2)*k1rx,P1.y()+(H/2)*k1ry,P3.x(),P3.y()))
    k2rx = k1rx + (H/2)*k1vx
    k2ry = k1ry + (H/2)*k1vy

    k3vx = acc(m3,P3.x(),P1.x()+(H/2)*k2rx,dist(P1.x()+(H/2)*k2rx,P1.y()+(H/2)*k2ry,P3.x(),P3.y()))
    k3vy = acc(m3,P3.y(),P1.y()+(H/2)*k2ry,dist(P1.x()+(H/2)*k2rx,P1.y()+(H/2)*k2ry,P3.x(),P3.y()))
    k3rx = k1rx + (H/2)*k2vx
    k3ry = k1ry + (H/2)*k2vy

    k4vx = acc(m3,P3.x(),P1.x()+(H)*k3rx,dist(P1.x()+(H)*k3rx,P1.y()+(H)*k3ry,P3.x(),P3.y()))
    k4vy = acc(m3,P3.y(),P1.y()+(H)*k3ry,dist(P1.x()+(H)*k3rx,P1.y()+(H)*k3ry,P3.x(),P3.y()))
    k4rx = k1rx + (H)*k3vx
    k4ry = k1ry + (H)*k3vy

    P1.calcpos(k1rx,k1ry,k2rx,k2ry,k3rx,k3ry,k4rx,k4ry)
    P1.calcvel(k1vx,k1vy,k2vx,k2vy,k3vx,k3vy,k4vx,k4vy)

    a = cosrule(dist(P1.x(),P1.y(),P3.x(),P3.y()),dist(P2.x(),P2.y(),P3.x(),P3.y()),
            dist(P1.x(),P1.y(),P2.x(),P2.y()))

    if eangle(a,dire(P2.x(),P2.y(),P3.x(),P3.y()),dire(P1.x(),P1.y(),P3.x(),P3.y())) == True:
        P1.deltav1(dist(P1.x(), P1.y(), P3.x(), P3.y()), (r_m),
                   angle(P1.x(), P1.y(), P3.x(), P3.y(), dire(P1.x(), P1.y(), P3.x(), P3.y())),
                   dire(P1.x(), P1.y(), P3.x(), P3.y()))
        print(a * (180 / math.pi))
        FIRST = False

    k = P1.tra
    if k == True:
        if TIMER == False:
            TIMER = True
            periodx = (period(dist(P1.x(), P1.y(), P3.x(), P3.y()), (r_m))) / 2
        P1.fal()

    if TIMER == True:
        T = T + 1

    if periodx - T <= 1 and periodx - T > 0:
        P1.deltav2((r_m),
                   angle(P1.x(), P1.y(), P3.x(), P3.y(), dire(P1.x(), P1.y(), P3.x(), P3.y())),
                   dire(P1.x(), P1.y(), P3.x(), P3.y()))
        print("Time of flight: ", T * H, "s")
        TIMER = False
        T = 0
        print(dist(P1.x(),P1.y(),P2.x(),P2.y()))

    P1.move()

    k1vx = acc(m3,P3.x(),P2.x(),dist(P2.x(),P2.y(),P3.x(),P3.y()))
    k1vy = acc(m3,P3.y(),P2.y(),dist(P2.x(),P2.y(),P3.x(),P3.y()))
    k1rx = P2.xv()
    k1ry = P2.yv()

    k2vx = acc(m3,P3.x(),P2.x()+(H/2)*k1rx,dist(P2.x()+(H/2)*k1rx,P2.y()+(H/2)*k1ry,P3.x(),P3.y()))
    k2vy = acc(m3,P3.y(),P2.y()+(H/2)*k1ry,dist(P2.x()+(H/2)*k1rx,P2.y()+(H/2)*k1ry,P3.x(),P3.y()))
    k2rx = k1rx + (H/2)*k1vx
    k2ry = k1ry + (H/2)*k1vy

    k3vx = acc(m3,P3.x(),P2.x()+(H/2)*k2rx,dist(P2.x()+(H/2)*k2rx,P2.y()+(H/2)*k2ry,P3.x(),P3.y()))
    k3vy = acc(m3,P3.y(),P2.y()+(H/2)*k2ry,dist(P2.x()+(H/2)*k2rx,P2.y()+(H/2)*k2ry,P3.x(),P3.y()))
    k3rx = k1rx + (H/2)*k2vx
    k3ry = k1ry + (H/2)*k2vy

    k4vx = acc(m3,P3.x(),P2.x()+(H)*k3rx,dist(P2.x()+(H)*k3rx,P2.y()+(H)*k3ry,P3.x(),P3.y()))
    k4vy = acc(m3,P3.y(),P2.y()+(H)*k3ry,dist(P2.x()+(H)*k3rx,P2.y()+(H)*k3ry,P3.x(),P3.y()))
    k4rx = k1rx + (H)*k3vx
    k4ry = k1ry + (H)*k3vy

    P2.calcpos(k1rx,k1ry,k2rx,k2ry,k3rx,k3ry,k4rx,k4ry)
    P2.calcvel(k1vx,k1vy,k2vx,k2vy,k3vx,k3vy,k4vx,k4vy)


    P2.move()

    pygame.display.update()
    FramePerSec.tick(FPS)