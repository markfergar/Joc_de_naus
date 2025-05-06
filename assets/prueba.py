import time
from pygame.locals import *
import pygame

AMPLADA = 800
ALTURA = 600
BACKGROUND_IMAGE = 'assets/fons.png'
MUSICA_FONS = 'assets/music.mp3'
RED = (255,0,0)
GREEN = (0,128,0)
BLUE = (0,0,255)
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

champi = pygame.image.load('assets/corazón_nave.png')
champi2 = pygame.image.load('assets/champi.png')

# Pantalla del joc
# Pantalla 1 - Menú
# Pantalla 2 - Crèdits
# Pantalla 3 - Joc
# Pantalla 4 - Game Over
pantalla_actual = 1

# Jugador 1:
player_image = pygame.image.load('assets/nau.png')
player_rect = player_image.get_rect(midbottom=(AMPLADA // 2, ALTURA - 70))
velocitat_nau = 5

# Jugador 2:
player_image2 = pygame.image.load('assets/enemic.png')
player_rect2 = player_image2.get_rect(midbottom=(AMPLADA // 2, ALTURA - 500))
velocitat_nau2 = 5

# vides:
vides_jugador1 = 3
vides_jugador2 = 3
vides_jugador1_image = champi2

# Bala rectangular blanca:
bala_imatge = pygame.Surface((4,10)) #definim una superficie rectangle de 4 pixels d'ample i 10 d'alçada
bala_imatge.fill(WHITE) #pintem la superficie de color blanc
bales_jugador1 = [] #llista on guardem les bales del jugador 1
bales_jugador2 = [] #llista on guardem les bales del jugador 2
velocitat_bales = 7  # Modificado de 5 a 7 para que vayan un poco más rápido
temps_entre_bales = 300  # Modificado de 500 a 300 para disparar con más frecuencia
temps_ultima_bala_jugador1 = 0 #per contar el temps que ha passat des de que ha disparat el jugador 1
temps_ultima_bala_jugador2 = 0 #per contar el temps que ha passat des de que ha disparat el jugador 2

pygame.init()
pantalla = pygame.display.set_mode((AMPLADA, ALTURA))
pygame.display.set_caption("Arcade 1vs1")

# Control de FPS
clock = pygame.time.Clock()
fps = 60

def imprimir_pantalla_fons(image):
    # Imprimeixo imatge de fons:
    background = pygame.image.load(image).convert()
    pantalla.blit(background, (0, 0))

def show_menu():
    imprimir_pantalla_fons(BACKGROUND_IMAGE)
    text0 = "SPACE UFOS!"
    text1 = "1. Començar partida"
    text2 = "2. Veure crèdits"
    text3 = "3. Sortir"
    font0 = pygame.font.SysFont(None, 140)
    font1 = pygame.font.SysFont(None, 100)
    img0 = font0.render(text0, True, YELLOW)  # Modificado a YELLOW para mejor contraste
    img1 = font1.render(text1, True, CYAN)    # Modificado a CYAN para mejor contraste
    img2 = font1.render(text2, True, WHITE)   # Modificado a WHITE para mejor contraste
    img3 = font1.render(text3, True, RED)     # Mantengo RED, ya contrasta bien
    pantalla.blit(img0, (60, 60))
    pantalla.blit(img1, (60, 200))
    pantalla.blit(img2, (60, 300))
    pantalla.blit(img3, (60, 400))

def show_credits():
    imprimir_pantalla_fons(BACKGROUND_IMAGE)
    text0 = "SPACE GUARS"
    text1 = "Programació:a"
    text2 = "Gràfics:"
    text3 = "Música:"
    text4 = "Sons:"
    text5 = "Mark Fernandez (i Xavi Sancho)"
    text6 = "After Burner 3 - Sega"
    text7 = "Freesound.org"
    font0 = pygame.font.SysFont(None, 140)
    font1 = pygame.font.SysFont(None, 60)
    font2 = pygame.font.SysFont(None, 50)
    img0 = font0.render(text0, True, PINK)
    img1 = font1.render(text1, True, WHITE)
    img2 = font1.render(text2, True, WHITE)
    img3 = font1.render(text3, True, WHITE)
    img4 = font1.render(text4, True, WHITE)
    img5 = font2.render(text5, True, BLACK)
    img6 = font2.render(text6, True, BLACK)
    img7 = font2.render(text7, True, PINK)
    pantalla.blit(img0, (60, 60))
    pantalla.blit(img1, (60, 200))
    pantalla.blit(img5, (160, 250))
    pantalla.blit(img2, (60, 300))
    pantalla.blit(img5, (160, 350))
    pantalla.blit(img3, (60, 400))
    pantalla.blit(img6, (160, 450))
    pantalla.blit(img4, (60, 500))
    pantalla.blit(img7, (160, 550))

while True:
    #contador
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if pantalla_actual == 2:
            show_credits()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pantalla_actual = 1

        # Menú
        if pantalla_actual == 1:
            if event.type == KEYDOWN:
                if event.key == K_3:
                    pygame.quit()
                if event.key == K_1:
                    pantalla_actual = 3
                if event.key == K_2:
                    pantalla_actual = 2

        if pantalla_actual == 4:
            for i in bales_jugador1:
                bales_jugador1.remove(i)
            for i in bales_jugador2:
                bales_jugador2.remove(i)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    vides_jugador1 = 3
                    vides_jugador2 = 3
                    pantalla_actual = 3

        if pantalla_actual == 3:
            # controlar trets de les naus
            if event.type == KEYDOWN:
                #jugador 1
                if event.key == K_w and current_time - temps_ultima_bala_jugador1 >= temps_entre_bales:
                    bales_jugador1.append(pygame.Rect(player_rect.centerx - 2, player_rect.top, 4, 10))
                    temps_ultima_bala_jugador1 = current_time
                # jugador 2
                if event.key == K_UP and current_time - temps_ultima_bala_jugador2 >= temps_entre_bales:
                    bales_jugador2.append(pygame.Rect(player_rect2.centerx - 2, player_rect2.bottom -10, 4, 10))
                    temps_ultima_bala_jugador2 = current_time

    if pantalla_actual == 4:
        imprimir_pantalla_fons('assets/gameover.png')
        text = "Player" + " " + str(guanyador)+ " " + "Wins!"
        font = pygame.font.SysFont(None, 60)
        img = font.render(text, True, WHITE)
        pantalla.blit(img, (250,500))

    if pantalla_actual == 1:
        show_menu()

    if pantalla_actual == 3:
        # Moviment del jugador 1
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            player_rect.x -= velocitat_nau
        if keys[K_d]:
            player_rect.x += velocitat_nau
        # Moviment del jugador 2
        if keys[K_LEFT]:
            player_rect2.x -= velocitat_nau2
        if keys[K_RIGHT]:
            player_rect2.x += velocitat_nau2

        # Mantenir al jugador dins de la pantalla:
        player_rect.clamp_ip(pantalla.get_rect())
        player_rect2.clamp_ip(pantalla.get_rect())

        #dibuixar el fons:
        imprimir_pantalla_fons(BACKGROUND_IMAGE)

        #Actualitzar i dibuixar les bales del jugador 1:
        for bala in bales_jugador1: # bucle que recorre totes les bales
            bala.y -= velocitat_bales # mou la bala
            if bala.bottom < 0 or bala.top > ALTURA: # comprova que no ha sortit de la pantalla
                bales_jugador1.remove(bala) # si ha sortit elimina la bala
            else:
                pantalla.blit(bala_imatge, bala) # si no ha sortit la dibuixa
            # Detectar col·lisions jugador 2:
            if player_rect2.colliderect(bala):  # si una bala toca al jugador1 (el seu rectangle)
                print("BOOM 1!")
                bales_jugador1.remove(bala)  # eliminem la bala
                vides_jugador2 = vides_jugador2 -1
                print("vides jugador 2:", vides_jugador2)
                # mostrem una explosió
                # eliminem el jugador 1 (un temps)
                # anotem punts al jugador 1

        # Actualitzar i dibuixar les bales del jugador 2:
        for bala in bales_jugador2:
            bala.y += velocitat_bales
            if bala.bottom < 0 or bala.top > ALTURA:
                bales_jugador2.remove(bala)
            else:
                pantalla.blit(bala_imatge, bala)
            # Detectar col·lisions jugador 1:
            if player_rect.colliderect(bala):  # si una bala toca al jugador1 (el seu rectangle)
                print("BOOM 2!")
                bales_jugador2.remove(bala)  # eliminem la bala
                vides_jugador1 = vides_jugador1 - 1
                print("vides jugador 1:",vides_jugador1)
                # mostrem una explosió
                # eliminem el jugador 1 (un temps)
                # anotem punts al jugador 1

        #dibuixar els jugadors:
        pantalla.blit(player_image, player_rect)
        pantalla.blit(player_image2, player_rect2)

        #dibuixar bales
        if vides_jugador1 >= 3:
            pantalla.blit(vides_jugador1_image, (680, 480))  # Modificado para más separación
        if vides_jugador1 >= 2:
            pantalla.blit(vides_jugador1_image, (720, 480))  # Modificado para más separación
        if vides_jugador1 >= 1:
            pantalla.blit(vides_jugador1_image, (760, 480))  # Modificado para más separación

        #dibuixar bales
        if vides_jugador2 >= 3:
            pantalla.blit(vides_jugador1_image, (20, 50))    # Modificado para más separación
        if vides_jugador2 >= 2:
            pantalla.blit(vides_jugador1_image, (60, 50))    # Modificado para más separación
        if vides_jugador2 >= 1:
            pantalla.blit(vides_jugador1_image, (100, 50))   # Modificado para más separación

        # Comprobem si algun jugador ha perdut totes les vides:
        if vides_jugador1 <=0 or vides_jugador2 <=0:
            ganyador = 1
            if vides_jugador1 <=0:
                guanyador = 2
            pantalla_actual = 4
    # No tocar
    pygame.display.update()
    clock.tick(fps)