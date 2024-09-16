import pygame, time
from os import system
from random import random
FoNt = 0
FoNtprint = 0
# pi = 3.14159265358979323

def cls():
    system("cls")
def font(face:str,size=18):
    global FoNt
    FoNt = pygame.font.SysFont(face,size)
def printpy(text:str,coords=(100,400),color=(128,128,128)):
    global FoNt,FoNtprint
    FoNtprint = FoNt.render(text,True,color)
    screen.blit(FoNtprint,coords)

def dist(p1, p2):
    return ( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 ) ** 0.5

screenRes = [1200, 800]
sCenter = pygame.math.Vector2(screenRes[0]/2, screenRes[1]/2)

cls()
verNum = int(input("Enter the number of Vertices sides of the abomination : "))
abomSize = int(input("How big of a Abomination do you need : "))

pygame.init()
screen = pygame.display.set_mode(screenRes)
#icon = pygame.image.load('')
pygame.display.set_caption("")
#pygame.display.set_icon(icon)

border = [10, 10]

g = pygame.math.Vector2((0, 98*3))
fric = 100

class abom:
    ver = list()
    e_wall = 0.9
    def __init__(self, mass, coords, vel) -> None:
        self.m = mass
        self.pos = coords
        self.vel = vel
        abom.ver.append(self)
    
    def draw(self) -> None:
        pygame.draw.polygon(screen, (123, 234, 196), [i.pos for i in abom.ver])

    def update(self, dt) -> None:
        self.vel += g*dt

        if isMousePressed == True:
            repForce = self.m * repCoeff/( (mpos-self.pos).magnitude_squared() + 1)
            repForce = pygame.math.Vector2(repForce)
            self.vel += repForce.rotate(repForce.angle_to(self.pos-mpos))*dt

        friction = pygame.math.Vector2(( min(fric*dt, self.vel.magnitude()) ))
        self.vel -= friction.rotate(friction.angle_to(self.vel))

        self.pos += self.vel*dt
        if not (border[0] < self.pos[0] < screenRes[0] - border[0]):
            self.pos[0] = max( min(self.pos[0], screenRes[0] - border[0]), border[0])
            self.vel[0] = -abom.e_wall*self.vel[0]
        if not (border[1] < self.pos[1] < screenRes[1] - border[1]):
            self.pos[1] = max( min(self.pos[1], screenRes[1] - border[1]), border[1])
            self.vel[1] = -abom.e_wall*self.vel[1]

verMaker = pygame.math.Vector2((0, abomSize))

for i in range(verNum):
    mass = 10
    velocity = pygame.math.Vector2((random()*100, random()*100))
    vertice = sCenter + verMaker.rotate(360*(i+1)/verNum)
    abom(mass, vertice, velocity)

class spring:
    all = list()
    def __init__(self, k, e1, e2) -> None:
        self.nl = dist(abom.ver[e1].pos, abom.ver[e2].pos) #natural length
        self.k = k   #spring constant
        self.start = e1 #start index in abom.ver
        self.end = e2   #end index in abom.ver
        spring.all.append(self)

    def update(self, dt):
        x = (abom.ver[self.start].pos - abom.ver[self.end].pos)
        x = x*(self.nl - x.magnitude())/(x.magnitude() + 0.01)
        force = self.k*x  #*(x.magnitude() ** 0.1)
        abom.ver[self.start].vel += force*dt/abom.ver[self.start].m
        abom.ver[self.end].vel -= force*dt/abom.ver[self.end].m
k = 600

for i in range(len(abom.ver)):
    for j in range(i + 1, len(abom.ver)):
        spring(k, i, j)

for i in range(len(abom.ver)-1, -1, -1):
    spring(k*10, i, i-1)

frameRate = 1000
dt = 1/1000

running = True
isMousePressed = False
repCoeff = 1900000
clock = pygame.time.Clock()
while running == True:
    initTime = time.time()
    clock.tick(frameRate*1.769)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            isMousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            isMousePressed = False
        
    #Code Here

    if isMousePressed == True:
        mpos = pygame.math.Vector2(pygame.mouse.get_pos())


    for i in range(len(spring.all)):
        spring.all[i].update(dt)

    for i in range(len(abom.ver)):
        abom.ver[i].update(dt)

    screen.fill((50, 50, 50))
    abom.draw(abom)
    pygame.display.update()


    endTime = time.time()
    dt = endTime-initTime
    if dt != 0: frameRate = 1/dt
    else: frameRate = 1000