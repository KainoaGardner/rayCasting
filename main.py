import math
from random import randint

import pygame

WIDTH = 1000
HEIGHT = 1000
FPS = 60


WHITE = "#ecf0f1"
GRAY = "#95a5a6"
BLACK = "#121212"
RED = (231, 76, 60)
YELLOW = (241, 196, 15)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


class Wall:
    def __init__(self, point1, point2, size, color):
        self.point1 = point1
        self.point2 = point2
        self.size = size
        self.color = color

    def display(self, screen):
        pygame.draw.line(screen, self.color, self.point1, self.point2, self.size)


def createWalls():
    walls = []
    for _ in range(5):
        point1 = (randint(0, WIDTH), randint(0, HEIGHT))
        point2 = (randint(0, WIDTH), randint(0, HEIGHT))

        walls.append(Wall(point1, point2, 5, WHITE))
    return walls


walls = createWalls()


class Light:
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.pos = [500.0, 500.0]
        self.speed = 10
        self.FOV = 360
        self.angle = 0
        self.distance = math.sqrt(WIDTH * WIDTH + HEIGHT * HEIGHT)

    def move(self):
        keys = pygame.key.get_pressed()
        xMove = self.speed * math.cos(math.radians(self.angle))
        yMove = self.speed * math.sin(math.radians(self.angle))

        if keys[pygame.K_w] and self.pos[1] > 0:
            self.pos[0] += xMove
            self.pos[1] += yMove
        if keys[pygame.K_s] and self.pos[1] < HEIGHT:
            self.pos[0] -= xMove
            self.pos[1] -= yMove

    def getPoint(self):
        pos = pygame.mouse.get_pos()
        xDif = pos[0] - self.pos[0]
        yDif = pos[1] - self.pos[1]

        self.angle = int(math.degrees(math.atan2(yDif, xDif)))

    def lineCollide(self, wall, rayPos):
        x1 = wall.point1[0]
        y1 = wall.point1[1]

        x2 = wall.point2[0]
        y2 = wall.point2[1]

        x3 = self.pos[0]
        y3 = self.pos[1]

        x4 = rayPos[0]
        y4 = rayPos[1]

        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if denominator == 0:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 0 < t < 1 and 0 < u:
            xCollide = x1 + t * (x2 - x1)
            yCollide = y1 + t * (y2 - y1)

            return (xCollide, yCollide)

        return False

    def update(self):
        self.getPoint()
        self.move()

    def displayLines(self, screen):
        for angle in range(-self.FOV // 2, self.FOV // 2 + 1):
            xPos = (
                self.distance * math.cos(math.radians(self.angle + angle)) + self.pos[0]
            )
            yPos = (
                self.distance * math.sin(math.radians(self.angle + angle)) + self.pos[1]
            )

            closestPoint = None
            smallestDistance = math.inf

            for wall in walls:
                point = self.lineCollide(wall, (xPos, yPos))
                if point:
                    xDif = point[0] - self.pos[0]
                    yDif = point[1] - self.pos[1]

                    distance = math.sqrt(xDif * xDif + yDif * yDif)
                    if distance < smallestDistance:
                        smallestDistance = distance
                        closestPoint = point

            if closestPoint:
                xPos = closestPoint[0]
                yPos = closestPoint[1]

            pygame.draw.line(
                screen,
                self.color,
                self.pos,
                (xPos, yPos),
                self.size // 10,
            )

    def display(self, screen):
        self.displayLines(screen)
        pygame.draw.circle(screen, WHITE, self.pos, self.size, 1)
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, YELLOW, pos, 5)


def display(screen, light, walls):
    screen.fill(BLACK)

    for wall in walls:
        wall.display(screen)

    light.display(screen)
    pygame.display.update()
    clock.tick(FPS)


def main():
    run = True
    light = Light(15, RED)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pass

        light.update()
        display(screen, light, walls)
        pygame.display.update()
        clock.tick(FPS)


main()
