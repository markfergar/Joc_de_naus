import pygame, sys
from pygame.locals import *

AMPLE = 1000
ALT = 800
TAMANY = (AMPLE,ALT)
RED = (255,0,0)
GREEN = (0,128,0)
BLUE = (0,150,255)
BLUE2 = (50,100,255)
INDIGO = (75,0,130)
ORANGE = (255,102,0)
YELLOW = (255,255,0)
VIOLET = (127,0,255)
GREY = (128,128,128)
MAROON = (128,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
OLIVE  =(128,128,0)
CYAN = (0,255,255)
PINK = (255,192,203)
MAGENTA = (128,0,128)
TAN = (210, 180, 128)
TEAL = (0,128,128)
u=0
i = 15
pygame.init()
pantalla = pygame.display.set_mode(TAMANY)
pygame.display.set_caption('Color de fons')
while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill(GREY)

    pygame.draw.circle(pantalla, BLACK, (500,400),350, 3)
    pygame.draw.circle(pantalla, BLUE, (500,400),348, 350)
    pygame.draw.circle(pantalla, BLACK, (500,475),275, 3)
    pygame.draw.circle(pantalla, WHITE, (500, 475), 273, 275)
    pygame.draw.circle(pantalla, RED, (500, 300), 50, 100)
    pygame.draw.circle(pantalla, BLACK, (400, 200), 100, 3)
    pygame.draw.circle(pantalla, WHITE, (400,200),97, 100)
    pygame.draw.circle(pantalla, BLACK, (600, 200), 100, 3)
    pygame.draw.circle(pantalla, WHITE, (600,200),97, 100)
    pygame.draw.line(pantalla, BLACK, (300, 400), (450, 390), 3)
    pygame.draw.line(pantalla, BLACK, (300, 450), (450, 450), 3)
    pygame.draw.line(pantalla, BLACK, (300, 500), (450, 510), 3)
    pygame.draw.line(pantalla, BLACK, (700, 400), (550, 390), 3)
    pygame.draw.line(pantalla, BLACK, (700, 450), (550, 450), 3)
    pygame.draw.line(pantalla, BLACK, (700, 500), (550, 510), 3)
    pygame.draw.rect(pantalla, RED, (275, 720, 450, 30))
    pygame.draw.circle(pantalla, YELLOW, (500, 760), 35, 0)
    pygame.draw.circle(pantalla, BLACK, (500, 760), 35, 3)
    pygame.draw.line(pantalla, BLACK, (500, 760), (500, 725), 3)
    pygame.draw.circle(pantalla, BLACK, (500, 760), 7, 0)
    rect_boca = pygame.Rect(350, 570, 300, 50)
    pygame.draw.arc(pantalla, BLACK, rect_boca, 3.14, 6.4, 5)
    pygame.draw.circle(pantalla, BLACK, (410, 230), 20, 12)
    pygame.draw.circle(pantalla, BLACK, (590, 230), 20, 12)


    pygame.display.update()
