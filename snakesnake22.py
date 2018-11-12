import pygame

RIGHT = 1
LEFT = -1
STOP = 0
UP = 2
DOWN = -2

FPS = 60
W = 700  # ширина экрана
H = 300  # высота экрана
GREEN = (210, 75, 150)
BLUE = (0, 70, 225)

pygame.init()
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# координаты и радиус круга
x = W // 2
y = H // 2
r = 50

motion = STOP

while 1:
    sc.fill(GREEN)

    pygame.draw.rect(sc, BLUE, ((x, y), (25, 25)))

    pygame.display.update()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                motion = LEFT
            elif i.key == pygame.K_RIGHT:
                motion = RIGHT
            elif i.key == pygame.K_UP:
                motion = UP
            elif i.key == pygame.K_DOWN:
                motion = DOWN
        elif i.type == pygame.KEYUP:
            if i.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
                         pygame.K_DOWN]:
                motion = STOP

    if motion == LEFT:
        x -= 3
    elif motion == RIGHT:
        x += 3
    elif motion == UP:
        y -= 3
    elif motion == DOWN:
        y += 3

    clock.tick(FPS)
