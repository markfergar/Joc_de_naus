import time
from pygame.locals import *
import pygame

# Constantes
AMPLADA = 800
ALTURA = 600
BACKGROUND_IMAGE = 'assets/fons.png'
MUSICA_FONS = 'assets/musica1.mp3'
MUSICA_JUEGO = 'assets/game_music.mp3'
MUSICA_GAMEOVER = 'assets/death_music.wav'
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
ORANGE = (255, 102, 0)
YELLOW = (255, 255, 0)
VIOLET = (127, 0, 255)
GREY = (128, 128, 128)
MAROON = (128, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
OLIVE = (128, 128, 0)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
MAGENTA = (128, 0, 128)
TAN = (210, 180, 128)
TEAL = (0, 128, 128)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((AMPLADA, ALTURA))
pygame.display.set_caption("Arcade 1vs1")

# Cargar imágenes
try:
    bala1 = pygame.image.load('assets/bala_nau.png')
    bala2 = pygame.image.load('assets/ñala.png')
    champi1 = pygame.image.load('assets/corazón_nave.png')
    champi2 = pygame.image.load('assets/champi.png')
    player_image = pygame.image.load('assets/nau.png')
    player_image2 = pygame.image.load('assets/enemic.png')
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    bala1 = pygame.Surface((4, 10))
    bala1.fill(WHITE)
    bala2 = pygame.Surface((4, 10))
    bala2.fill(RED)
    champi1 = pygame.Surface((30, 30))
    champi1.fill(RED)
    champi2 = pygame.Surface((30, 30))
    champi2.fill(GREEN)
    player_image = pygame.Surface((50, 50))
    player_image.fill(BLUE)
    player_image2 = pygame.Surface((50, 50))
    player_image2.fill(RED)

# Escalar las imágenes de las vidas a 60x60 píxeles
vides_jugador1_image = pygame.transform.scale(champi2, (60, 60))
vides_jugador2_image = pygame.transform.scale(champi1, (60, 60))

# Jugadores
player_rect = player_image.get_rect(midbottom=(AMPLADA // 2, ALTURA - 70))
velocitat_nau = 5
player_rect2 = player_image2.get_rect(midbottom=(AMPLADA // 2, ALTURA - 500))
velocitat_nau2 = 5

# Vidas
vides_jugador1 = 3
vides_jugador2 = 3

# Bales
bala_imatge = pygame.Surface((4, 10))
bala_imatge.fill(WHITE)
bales_jugador1 = []
bales_jugador2 = []
velocitat_bales = 7
temps_entre_bales = 300
temps_ultima_bala_jugador1 = 0
temps_ultima_bala_jugador2 = 0

# Pantalla actual
pantalla_actual = 1

# Control de FPS
clock = pygame.time.Clock()
fps = 60

# Cargar música del menú al inicio
pygame.mixer.music.load(MUSICA_FONS)
pygame.mixer.music.play(-1)  # Reproducir en bucle

def imprimir_pantalla_fons(image):
    try:
        background = pygame.image.load(image).convert()
        pantalla.blit(background, (0, 0))
    except pygame.error as e:
        print(f"Error al cargar fondo: {e}")
        pantalla.fill(BLACK)

def show_menu():
    imprimir_pantalla_fons(BACKGROUND_IMAGE)
    text0 = "SPACE UFOS!"
    text1 = "1. Començar partida"
    text2 = "2. Veure crèdits"
    text3 = "3. Sortir"
    font0 = pygame.font.SysFont(None, 140)
    font1 = pygame.font.SysFont(None, 100)
    img0 = font0.render(text0, True, GREEN)
    img1 = font1.render(text1, True, MAGENTA)
    img2 = font1.render(text2, True, MAGENTA)
    img3 = font1.render(text3, True, RED)
    pantalla.blit(img0, (60, 60))
    pantalla.blit(img1, (60, 200))
    pantalla.blit(img2, (60, 300))
    pantalla.blit(img3, (60, 400))

def show_credits():
    imprimir_pantalla_fons(BACKGROUND_IMAGE)
    text0 = "SPACE GUARS"
    text1 = "Programació:"
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

# Bucle principal
while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if pantalla_actual == 1:  # Menú
            if event.type == KEYDOWN:
                if event.key == K_3:
                    pygame.quit()
                    exit()
                if event.key == K_1:
                    pantalla_actual = 3
                    pygame.mixer.music.load(MUSICA_JUEGO)
                    pygame.mixer.music.play(-1)
                if event.key == K_2:
                    pantalla_actual = 2

        if pantalla_actual == 2:  # Créditos
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pantalla_actual = 1
                    pygame.mixer.music.load(MUSICA_FONS)
                    pygame.mixer.music.play(-1)

        if pantalla_actual == 3:  # Juego
            if event.type == KEYDOWN:
                # Jugador 1
                if event.key == K_w and current_time - temps_ultima_bala_jugador1 >= temps_entre_bales:
                    bales_jugador1.append(pygame.Rect(player_rect.centerx - 2, player_rect.top, 4, 10))
                    temps_ultima_bala_jugador1 = current_time
                # Jugador 2
                if event.key == K_UP and current_time - temps_ultima_bala_jugador2 >= temps_entre_bales:
                    bales_jugador2.append(pygame.Rect(player_rect2.centerx - 2, player_rect2.bottom - 10, 4, 10))
                    temps_ultima_bala_jugador2 = current_time

        if pantalla_actual == 4:  # Game Over
            for i in bales_jugador1[:]:
                bales_jugador1.remove(i)
            for i in bales_jugador2[:]:
                bales_jugador2.remove(i)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # Reiniciar juego
                    vides_jugador1 = 3
                    vides_jugador2 = 3
                    player_rect.midbottom = (AMPLADA // 2, ALTURA - 70)
                    player_rect2.midbottom = (AMPLADA // 2, ALTURA - 500)
                    pantalla_actual = 3
                    pygame.mixer.music.load(MUSICA_JUEGO)
                    pygame.mixer.music.play(-1)
                if event.key == K_ESCAPE:  # Volver al menú
                    vides_jugador1 = 3
                    vides_jugador2 = 3
                    player_rect.midbottom = (AMPLADA // 2, ALTURA - 70)
                    player_rect2.midbottom = (AMPLADA // 2, ALTURA - 500)
                    pantalla_actual = 1
                    pygame.mixer.music.load(MUSICA_FONS)
                    pygame.mixer.music.play(-1)

    # Limpiar pantalla
    pantalla.fill(BLACK)

    if pantalla_actual == 1:  # Menú
        show_menu()

    if pantalla_actual == 2:  # Créditos
        show_credits()

    if pantalla_actual == 3:  # Juego
        # Movimiento del jugador 1
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            player_rect.x -= velocitat_nau
        if keys[K_d]:
            player_rect.x += velocitat_nau
        # Movimiento del jugador 2
        if keys[K_LEFT]:
            player_rect2.x -= velocitat_nau2
        if keys[K_RIGHT]:
            player_rect2.x += velocitat_nau2

        # Mantener a los jugadores dentro de la pantalla
        player_rect.clamp_ip(pantalla.get_rect())
        player_rect2.clamp_ip(pantalla.get_rect())

        # Dibujar el fondo
        imprimir_pantalla_fons(BACKGROUND_IMAGE)

        # Actualizar y dibujar las balas del jugador 1
        for bala in bales_jugador1[:]:
            bala.y -= velocitat_bales
            if bala.bottom < 0 or bala.top > ALTURA:
                bales_jugador1.remove(bala)
            else:
                pantalla.blit(bala1, bala)
            # Detectar colisiones con jugador 2
            if player_rect2.colliderect(bala):
                print("BOOM 1!")
                bales_jugador1.remove(bala)
                vides_jugador2 -= 1
                print("Vides jugador 2:", vides_jugador2)

        # Actualizar y dibujar las balas del jugador 2
        for bala in bales_jugador2[:]:
            bala.y += velocitat_bales
            if bala.bottom < 0 or bala.top > ALTURA:
                bales_jugador2.remove(bala)
            else:
                pantalla.blit(bala2, bala)
            # Detectar colisiones con jugador 1
            if player_rect.colliderect(bala):
                print("BOOM 2!")
                bales_jugador2.remove(bala)
                vides_jugador1 -= 1
                print("Vides jugador 1:", vides_jugador1)

        # Dibujar los jugadores
        pantalla.blit(player_image, player_rect)
        pantalla.blit(player_image2, player_rect2)

        # Dibujar vidas del jugador 1 (inferior derecha)
        if vides_jugador1 >= 3:
            pantalla.blit(vides_jugador1_image, (600, 480))
        if vides_jugador1 >= 2:
            pantalla.blit(vides_jugador1_image, (660, 480))
        if vides_jugador1 >= 1:
            pantalla.blit(vides_jugador1_image, (720, 480))

        # Dibujar vidas del jugador 2 (superior izquierda)
        if vides_jugador2 >= 3:
            pantalla.blit(vides_jugador2_image, (0, 50))
        if vides_jugador2 >= 2:
            pantalla.blit(vides_jugador2_image, (60, 50))
        if vides_jugador2 >= 1:
            pantalla.blit(vides_jugador2_image, (120, 50))

        # Comprobar si algún jugador ha perdido todas las vidas
        if vides_jugador1 <= 0 or vides_jugador2 <= 0:
            guanyador = 1 if vides_jugador2 <= 0 else 2
            pantalla_actual = 4
            pygame.mixer.music.load(MUSICA_GAMEOVER)
            pygame.mixer.music.play()

    if pantalla_actual == 4:  # Game Over
        imprimir_pantalla_fons('assets/gameover.png')
        text = f"Player {guanyador} Wins!"
        font = pygame.font.SysFont(None, 60)
        img = font.render(text, True, WHITE)
        pantalla.blit(img, (250, 500))

    # Actualizar pantalla
    pygame.display.update()
    clock.tick(fps)
