import pygame
import random
import math
import pdb

number_of_particles = 10
background_colour = (255,255,255)
velo_line_colour = (255,0,0)
force_line_colour = (100,0,255)
(width, height) = (1000, 1000)
drag = 1
elasticity = 1
gravity = (math.pi, 0.00)
G = 1

def addVectors((angle1, length1), (angle2, length2)):
    x  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    y  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    # print "x=", x
    # print "y=", y
    angle = math.atan2(y, x)
    length  = math.hypot(x, y)
    # print "angle=", angle
    # print "length=", length
    # cos = a/h sin = o/h tan = o/a = (o/h)*(h/a)

    return (angle, length)


def distanceVector(a,b):
    x = b.x - a.x
    y = b.y - a.y
    angle = math.atan2(y,x)
    magnitude = math.hypot(x,y)
    return (angle, magnitude)

def gForce(particle):
    resultant = (0,0)
    for other in my_particles:
        if other != particle:
            gMag = G*other.mass/(distanceVector(particle,other)[1]**2)
            # print "gMag=", gMag
            gArg = distanceVector(particle,other)[0]
            # print "gARG=", gArg
            resultant = addVectors(resultant,(gArg, gMag))
    # print resultant
    return resultant

class Particle():
    def __init__(self, (x, y), size):
        self.x = x
        self.y = y
        self.size = size
        self.mass = size*size
        self.colour = (0, 0, 255)
        self.thickness = 2
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
            
        vHyp = 30#2.0*self.size*self.speed/5
        vEnd = (self.x+vHyp*math.cos(self.angle), self.y + vHyp*math.sin(self.angle))
        pygame.draw.aaline(screen, velo_line_colour, (self.x, self.y), vEnd)

        self.f = gForce(self)
        fHyp = 30#2.0*self.size*f[1]*300
        fEnd = (self.x + fHyp*math.cos(self.f[0]), self.y + fHyp*math.sin(self.f[0]))
        pygame.draw.aaline(screen, force_line_colour, (self.x, self.y), fEnd)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        (self.angle, self.speed) = addVectors((self.angle, self.speed), self.f)#gForce(self))
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = 2*math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = 2*math.pi - self.angle
            self.speed *= elasticity

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('N-Bodies Interacting Via Gravity')

my_particles = []

for n in range(number_of_particles):
    size = random.randint(10, 20)
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)

    # x = random.randint(600,800)
    # y = random.randint(600,800)

    # x = 400 + 200*(n)
    # y = 400 + 200*n

    particle = Particle((x, y), size)
    particle.speed = random.uniform(.3,1)
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

running = True
first = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_colour)

    toggle = 1
    
    for particle in my_particles:
        #if first:
        particle.display()
        particle.move()
        particle.bounce()
    
        # if toggle == 1:
        #     print particle.f[0]*180/math.pi
        #     toggle = 0
        # else:
        #     toggle = 1
    #pdb.set_trace()
    first = False
    pygame.display.flip()