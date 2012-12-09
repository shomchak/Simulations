# Simulates n point masses orbiting around a fixed mass at the center, interacting
# with gravity. The positions of the masses are initialized with radial symmetry.
# The masses can pass through each other. The red and blue lines point in the 
# direction of the velocity vector and force vector, respectively. 


import pygame
import random
import math
import pdb

running = True
number_of_particles = 2
background_colour = (255,255,255)
velo_line_colour = (255,0,0)
force_line_colour = (100,0,255)
(width, height) = (1000, 1000)
drag = 1
elasticity = 1
gravity = (math.pi, 0.00)
G = .7
trace = True 
timestep = 1

def addVectors(v1, v2):
    angle1 = v1[0]
    length1 = v1[1]
    angle2 = v2[0]
    length2 = v2[1]
    x  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    y  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    angle = math.atan2(y, x)
    length  = math.hypot(x, y)
    return [angle, length]

def distanceVector(a,b):
    x = b.x - a.x
    y = b.y - a.y
    angle = math.atan2(y,x)
    magnitude = math.hypot(x,y)
    return (angle, magnitude)

def acceleration(particle):
    resultant = [0,0]
    for other in my_particles:
        if other != particle:
            gMag = G*other.mass/(distanceVector(particle,other)[1]**2)
            gArg = distanceVector(particle,other)[0]
            resultant = addVectors(resultant,[gArg, gMag])
    return resultant

def eulerIntegrate(particle,dt):
    x = particle.x + dt * particle.speed * math.cos(particle.angle)
    y = particle.y + dt * particle.speed * math.sin(particle.angle)
    [angle,speed] = addVectors([particle.angle,particle.speed],particle.f)
    particle.x = x
    particle.y = y
    particle.angle = angle
    particle.speed = speed

def rungeKutta4(particle,dt):
    x0 = particle.x
    y0 = particle.y
    s0 = particle.speed
    a0 = particle.angle

    x1 = x0
    y1 = y0
    a1 = a0
    s1 = s0
    acc1 = acceleration(particle)

    x2 = x0 + 0.5 * s1 * math.cos(a1) * dt
    y2 = y0 + 0.5 * s1 * math.sin(a1) * dt
    (a2,s2) = addVectors([a1,s1],[acc1[0],acc1[1]*0.5*dt])
    particle.x = x2
    particle.y = y2
    acc2 = acceleration(particle)

    x3 = x0 + 0.5 * s2 * math.cos(a2) * dt
    y3 = y0 + 0.5 * s2 * math.sin(a2) * dt
    (a3,s3) = addVectors([a2,s2],[acc2[0],acc2[1]*0.5*dt])
    particle.x = x3
    particle.y = y3
    acc3 = acceleration(particle)

    x4 = x0 + s3 * math.cos(a3) * dt
    y4 = y0 + s3 * math.sin(a3) * dt
    (a4,s4) = addVectors([a3,s3],[acc3[0],acc3[1]*dt])
    particle.x = x4
    particle.y = y4
    acc4 = acceleration(particle)

    xf = x0 + (dt/6.0)*(s1*math.cos(a1)+2.0*s2*math.cos(a2)+2.0*s3*math.cos(a3)+s4*math.cos(a4))
    yf = y0 + (dt/6.0)*(s1*math.sin(a1)+2.0*s2*math.sin(a2)+2.0*s3*math.sin(a3)+s4*math.sin(a4))
    (af,sf) = addVectors([a0,s0],addVectors([acc1[0],acc1[1]*dt/6.0],addVectors([acc2[0],acc2[1]*2.0*dt/6.0],addVectors([acc3[0],acc3[1]*2.0*dt/6.0],[acc4[0],acc4[1]*dt/6.0]))))

    particle.x = xf
    particle.y = yf
    particle.angle = af
    particle.speed = sf

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

        self.f = acceleration(self)
        fHyp = 30#2.0*self.size*f[1]*300
        fEnd = (self.x + fHyp*math.cos(self.f[0]), self.y + fHyp*math.sin(self.f[0]))
        pygame.draw.aaline(screen, force_line_colour, (self.x, self.y), fEnd)

    def move(self):
        # eulerIntegrate(self,timestep)
        rungeKutta4(self,timestep)
        self.speed *= drag
        self.bounce()

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
    size = 15#random.randint(10, 20)
    # x = random.randint(size, width-size)
    # y = random.randint(size, height-size)

    # x = random.randint(600,800)
    # y = random.randint(600,800)
    radius = 300
    x = width/2 + radius*math.cos(2*math.pi*n/number_of_particles)
    y = height/2 + radius*math.sin(2*math.pi*n/number_of_particles)
    particle = Particle((x, y), size)
    particle.speed = 3
    particle.angle = 2*math.pi*n/number_of_particles + math.pi/2

    # x = 300 + 400*n
    # y = 500
    # particle = Particle((x, y), size)

    # particle.speed = 3#random.uniform(1,2)
    # particle.angle = -math.pi/2#random.uniform(0, math.pi*2)

    my_particles.append(particle)

fixed = Particle((width/2,height/2),30)
fixed.mass = 9000
my_particles.append(fixed)

if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(background_colour)
        toggle = 1
        for particle in my_particles:
            particle.display()
        for particle in my_particles:
            if particle != fixed:
                particle.move()
                # particle.bounce()
        pygame.display.flip()