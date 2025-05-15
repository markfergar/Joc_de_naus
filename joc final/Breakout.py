import pygame
import random
import os
import math

# Inicializar Pygame
try:
    pygame.init()
except Exception as e:
    print(f"Error al inicializar Pygame: {e}")
    exit()

# Configuración de la ventana y el mundo
WINDOW_WIDTH = 800
HEIGHT = 600
WORLD_WIDTH = 2400
try:
    window = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
    pygame.display.set_caption("Juego de MARAL")
except Exception as e:
    print(f"Error al configurar la ventana: {e}")
    exit()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
TRANS_BLACK = (0, 0, 0, 128)

# Fuente
try:
    font = pygame.font.Font(None, 36)
except Exception as e:
    print(f"Error al cargar la fuente: {e}")
    font = pygame.font.SysFont("Arial", 36)

# Cargar imagen de vida
try:
    vida_img = pygame.image.load("assets/vida_jugador1.png").convert_alpha()
    vida_img = pygame.transform.scale(vida_img, (40, 40))
except pygame.error as e:
    print(f"Error loading 'assets/vida_jugador1.png': {e}")
    vida_img = pygame.Surface((40, 40))
    vida_img.fill(RED)

# Cargar fondo principal
try:
    background_img = pygame.image.load("assets/fons.png").convert()
    background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading 'assets/fons.png': {e}")
    background_img = pygame.Surface((WINDOW_WIDTH, HEIGHT))
    background_img.fill((135, 206, 235))

# Clase para las nubes
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.base_image = pygame.image.load("assets/cloud.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading 'assets/cloud.png': {e}")
            self.base_image = pygame.Surface((100, 50), pygame.SRCALPHA)
            pygame.draw.circle(self.base_image, WHITE, (50, 25), 25)
            self.base_image.set_colorkey((0, 0, 0))
        # Escalar aleatoriamente entre 50x50 y 150x150
        scale_factor = random.uniform(0.5, 1.5)
        self.image = pygame.transform.scale(self.base_image, (int(self.base_image.get_width() * scale_factor), int(self.base_image.get_height() * scale_factor)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-100, WINDOW_WIDTH + 100)  # Posición inicial aleatoria
        self.rect.y = random.randint(50, 200)  # Altura entre 50 y 200
        self.speed = 1.0 * random.choice([-1, 1])  # Velocidad fija de 1.0, dirección aleatoria

    def update(self):
        self.rect.x += self.speed
        # Reaparecer en el lado opuesto
        if self.rect.right < 0:  # Si sale por la izquierda
            self.rect.x = WINDOW_WIDTH  # Reaparece por la derecha
            self.rect.y = random.randint(50, 200)  # Nueva altura aleatoria
            scale_factor = random.uniform(0.5, 1.5)  # Nuevo tamaño aleatorio
            self.image = pygame.transform.scale(self.base_image, (int(self.base_image.get_width() * scale_factor), int(self.base_image.get_height() * scale_factor)))
        if self.rect.left > WINDOW_WIDTH:  # Si sale por la derecha
            self.rect.x = 0 - self.rect.width  # Reaparece por la izquierda
            self.rect.y = random.randint(50, 200)  # Nueva altura aleatoria
            scale_factor = random.uniform(0.5, 1.5)  # Nuevo tamaño aleatorio
            self.image = pygame.transform.scale(self.base_image, (int(self.base_image.get_width() * scale_factor), int(self.base_image.get_height() * scale_factor)))

# Clase para efecto de recolección de moneda
class CoinEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for radius in range(5, 25, 5):
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, YELLOW, (radius, radius), radius)
            self.frames.append(surface)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_duration = 3

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_index]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

# Clase para la explosión
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        self.frame_index = 0
        for radius in range(10, 60, 10):
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            color = [RED, ORANGE, YELLOW, ORANGE, RED][radius // 10 - 1]
            pygame.draw.circle(surface, color, (radius, radius), radius)
            self.frames.append(surface)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_timer = 0
        self.frame_duration = 5

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame_index]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

# Clase del Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar imágenes de movimiento
        try:
            self.steve_movimiento_1 = pygame.image.load("assets/steve_movimiento_1.png").convert_alpha()
            print("Cargada steve_movimiento_1.png correctamente")
        except pygame.error as e:
            print(f"Error al cargar 'steve_movimiento_1.png': {e}")
            self.steve_movimiento_1 = pygame.Surface((40, 70))
            self.steve_movimiento_1.fill(BLUE)
            print("Usando superficie azul como respaldo para steve_movimiento_1.png")

        try:
            self.steve_movimiento_2 = pygame.image.load("assets/steve_movimiento_2.png").convert_alpha()
            print("Cargada steve_movimiento_2.png correctamente")
        except pygame.error as e:
            print(f"Error al cargar 'steve_movimiento_2.png': {e}")
            self.steve_movimiento_2 = pygame.Surface((40, 70))
            self.steve_movimiento_2.fill(BLUE)
            print("Usando superficie azul como respaldo para steve_movimiento_2.png")

        # Cargar imágenes de parado
        try:
            self.steve_parado_1 = pygame.image.load("assets/steve_parado_1.png").convert_alpha()
            print("Cargada steve_parado_1.png correctamente")
        except pygame.error as e:
            print(f"Error al cargar 'steve_parado_1.png': {e}")
            self.steve_parado_1 = pygame.Surface((40, 70))
            self.steve_parado_1.fill(BLUE)
            print("Usando superficie azul como respaldo para steve_parado_1.png")

        try:
            self.steve_parado_2 = pygame.image.load("assets/steve_parado_2.png").convert_alpha()
            print("Cargada steve_parado_2.png correctamente")
        except pygame.error as e:
            print(f"Error al cargar 'steve_parado_2.png': {e}")
            self.steve_parado_2 = pygame.Surface((40, 70))
            self.steve_parado_2.fill(BLUE)
            print("Usando superficie azul como respaldo para steve_parado_2.png")

        # Escalar imágenes
        self.steve_movimiento_1 = pygame.transform.scale(self.steve_movimiento_1, (40, 70))
        self.steve_movimiento_2 = pygame.transform.scale(self.steve_movimiento_2, (40, 70))
        self.steve_parado_1 = pygame.transform.scale(self.steve_parado_1, (40, 70))
        self.steve_parado_2 = pygame.transform.scale(self.steve_parado_2, (40, 70))

        # Imágenes para animación
        self.walk_left = [self.steve_movimiento_1, self.steve_parado_1]
        self.walk_right = [self.steve_movimiento_2, self.steve_parado_2]
        self.stand_left = [self.steve_parado_1]
        self.stand_right = [self.steve_parado_2]

        self.image = self.stand_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH // 2 - self.rect.width // 2
        self.rect.bottom = HEIGHT - 20
        self.vel_x = 0
        self.vel_y = 0
        self.jumping = False
        self.direction = "right"
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_duration = 6
        self.score = 0
        self.lives = 2

    def update(self, platforms, enemies, explosions):
        # Gravedad
        self.vel_y += 0.5
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        # Movimiento horizontal
        self.rect.x += self.vel_x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WORLD_WIDTH - self.rect.width:
            self.rect.x = WORLD_WIDTH - self.rect.width

        # Animación
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % 2

        if self.vel_x != 0:
            if self.vel_x > 0:
                self.image = self.walk_right[self.frame_index]
                self.direction = "right"
            else:
                self.image = self.walk_left[self.frame_index]
                self.direction = "left"
        else:
            self.image = self.stand_right[0] if self.direction == "right" else self.stand_left[0]

        # Colisiones con plataformas
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.vel_y > 0:  # Cayendo
                if self.rect.bottom > platform.rect.top and self.rect.bottom <= platform.rect.top + 20:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.jumping = False
            elif self.vel_y < 0:  # Saltando
                if self.rect.top < platform.rect.bottom and self.rect.top >= platform.rect.bottom - 20:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Colisiones con enemigos
        enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in enemy_hits:
            self.lives -= 1
            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
            explosions.add(explosion)
            enemy.respawn(self.rect.x, enemies)
            if self.lives <= 0:
                return "game_over"

        return False

    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            self.jumping = True

# Clase Plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, 20))
        self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Clase Moneda
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
        except pygame.error as e:
            print(f"Error loading 'assets/coin.png': {e}")
            self.image = pygame.Surface((20, 20))
            self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collect_radius = 40

# Clase Enemigo (Creeper)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, move_range=300, zone_start=0, zone_end=2400, follow_player=False, level=1):
        super().__init__()
        try:
            self.base_image = pygame.image.load("assets/creeper.png").convert_alpha()
            self.base_image = pygame.transform.scale(self.base_image, (40, 70))
        except pygame.error as e:
            print(f"Error loading 'assets/creeper.png': {e}")
            self.base_image = pygame.Surface((40, 70), pygame.SRCALPHA)
            self.base_image.fill(GREEN)

        self.walk_right = [self.base_image for _ in range(2)]
        self.walk_left = [pygame.transform.flip(self.base_image, True, False) for _ in range(2)]

        self.image = self.walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        # Aumentar la velocidad base según el nivel (50% más por nivel)
        base_speed = random.choice([-2, 2])
        self.vel_x = base_speed * (1 + (level - 1) * 0.5)
        self.frame = 0
        self.direction = "right" if self.vel_x > 0 else "left"
        self.start_x = x
        self.move_range = move_range
        self.zone_start = zone_start
        self.zone_end = zone_end
        self.follow_player = follow_player
        self.level = level
        self.base_speed = abs(base_speed) * (1 + (level - 1) * 0.5)  # Guardar velocidad base para persecución

    def update(self, player_x=None, player_y=None):
        # Definir los límites del rango de movimiento
        left_limit = max(self.start_x - self.move_range, self.zone_start)
        right_limit = min(self.start_x + self.move_range, self.zone_end - self.rect.width)

        if self.follow_player and player_x is not None and player_y is not None:
            # Calcular distancias
            distance_x = abs(player_x - self.rect.x)
            distance_y = abs(player_y - self.rect.y)

            # Si el jugador está dentro del rango del enemigo, perseguirlo
            if left_limit <= player_x <= right_limit:
                # Detenerse si está muy cerca (10 píxeles horizontalmente y 20 píxeles verticalmente)
                if distance_x < 10 and distance_y < 20:
                    self.vel_x = 0
                else:
                    # Moverse hacia el jugador a velocidad normal
                    if player_x > self.rect.x:
                        self.vel_x = self.base_speed  # Moverse a la derecha
                    elif player_x < self.rect.x:
                        self.vel_x = -self.base_speed  # Moverse a la izquierda
            else:
                # Si el jugador está fuera del rango, patrullar dentro del rango
                if self.rect.x <= left_limit:
                    self.vel_x = self.base_speed  # Cambiar a dirección positiva (derecha)
                elif self.rect.x >= right_limit:
                    self.vel_x = -self.base_speed  # Cambiar a dirección negativa (izquierda)

        else:
            # Lógica para enemigos que patrullan (no siguen al jugador)
            if self.rect.x <= left_limit:
                self.rect.x = left_limit
                self.vel_x = abs(self.vel_x)  # Cambiar a dirección positiva (derecha)
            elif self.rect.x >= right_limit:
                self.rect.x = right_limit
                self.vel_x = -abs(self.vel_x)  # Cambiar a dirección negativa (izquierda)

        # Aplicar movimiento
        self.rect.x += self.vel_x

        # Asegurarse de que no se salga de los límites
        if self.rect.x <= left_limit:
            self.rect.x = left_limit
            if self.follow_player and player_x is not None:
                self.vel_x = self.base_speed if player_x > self.rect.x else self.vel_x
            else:
                self.vel_x = abs(self.vel_x)
        elif self.rect.x >= right_limit:
            self.rect.x = right_limit
            if self.follow_player and player_x is not None:
                self.vel_x = -self.base_speed if player_x < self.rect.x else self.vel_x
            else:
                self.vel_x = -abs(self.vel_x)

        # Actualizar animación
        self.frame += 0.1
        if self.frame >= 2:
            self.frame = 0

        if self.vel_x > 0:
            self.image = self.walk_right[int(self.frame)]
            self.direction = "right"
        elif self.vel_x < 0:
            self.image = self.walk_left[int(self.frame)]
            self.direction = "left"

    def respawn(self, player_x, enemies):
        new_x = random.randint(self.zone_start, self.zone_end - 40)
        while abs(new_x - player_x) < 100:
            new_x = random.randint(self.zone_start, self.zone_end - 40)
        for enemy in enemies:
            if enemy != self and abs(new_x - enemy.rect.x) < 50:
                new_x = random.randint(self.zone_start, self.zone_end - 40)
        self.rect.x = new_x
        self.start_x = new_x  # Actualizar start_x para que los límites se calculen correctamente
        base_speed = random.choice([-2, 2])
        self.vel_x = base_speed * (1 + (self.level - 1) * 0.5)
        self.base_speed = abs(base_speed) * (1 + (self.level - 1) * 0.5)  # Actualizar velocidad base
        self.rect.bottom = HEIGHT - 20

# Definición de niveles
def create_level(level_num):
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    coin_effects = pygame.sprite.Group()

    player = Player()
    player.score = 0
    all_sprites.add(player)

    ground = Platform(0, HEIGHT - 20, WORLD_WIDTH)
    platforms.add(ground)
    all_sprites.add(ground)

    levels = [
        [Platform(200, 450, 200), Platform(500, 350, 250), Platform(800, 250, 200),
         Platform(1100, 400, 200), Platform(1400, 300, 250), Platform(1700, 200, 200),
         Platform(2000, 350, 200)],
        [Platform(100, 450, 400), Platform(600, 400, 300), Platform(1000, 450, 350),
         Platform(1400, 400, 400), Platform(1900, 450, 300)],
        [Platform(150, 450, 200), Platform(400, 350, 200), Platform(650, 450, 200),
         Platform(900, 300, 250), Platform(1200, 400, 200), Platform(1500, 250, 200),
         Platform(1800, 350, 250), Platform(2100, 450, 200)]
    ]

    for plat in levels[level_num - 1]:
        platforms.add(plat)
        all_sprites.add(plat)

    num_coins = 10 + level_num * 2
    platform_list = [ground] + levels[level_num - 1]
    for _ in range(num_coins):
        valid_position = False
        attempts = 0
        while not valid_position and attempts < 50:
            platform = random.choice(platform_list)
            coin_x = random.randint(platform.rect.left, platform.rect.right - 20)
            coin_y = platform.rect.top - random.randint(30, 80)
            if coin_y < 50:
                coin_y = platform.rect.top - 30
            coin = Coin(coin_x, coin_y)
            coin.rect.x = coin_x
            coin.rect.y = coin_y
            collides = any(coin.rect.colliderect(plat.rect) for plat in platforms)
            if not collides:
                valid_position = True
                coins.add(coin)
                all_sprites.add(coin)
            attempts += 1

    if level_num == 1:
        num_enemies = 2
        num_followers = 2
    elif level_num == 2:
        num_enemies = 4
        num_followers = 2
    else:
        num_enemies = 5
        num_followers = 3

    # Ajustar las zonas para que sean más amplias y no se solapen
    zone_width = WORLD_WIDTH // num_enemies
    enemy_zones = []
    for i in range(num_enemies):
        zone_start = i * zone_width
        zone_end = (i + 1) * zone_width
        # Asegurar que las zonas no se solapen y tengan un tamaño mínimo
        if i > 0:
            zone_start = max(zone_start, enemy_zones[i-1][1] + 50)  # Separación mínima de 50 píxeles
        enemy_zones.append((zone_start, zone_end))

    for i in range(num_enemies):
        zone_start, zone_end = enemy_zones[i]
        enemy_x = random.randint(zone_start, zone_end - 40)
        while abs(enemy_x - player.rect.x) < 100:
            enemy_x = random.randint(zone_start, zone_end - 40)
        follow = i < num_followers
        # Ajustar move_range para que sea proporcional al tamaño de la zona
        move_range = (zone_end - zone_start) // 2
        enemy = Enemy(enemy_x, HEIGHT - 20, move_range=move_range, zone_start=zone_start, zone_end=zone_end, follow_player=follow, level=level_num)
        enemy.level = level_num
        enemies.add(enemy)
        all_sprites.add(enemy)

    return all_sprites, platforms, coins, enemies, player, explosions, coin_effects

# Pantalla de victoria
def win_screen():
    try:
        win_img = pygame.image.load("assets/win1.png").convert()
        win_img = pygame.transform.scale(win_img, (WINDOW_WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading 'assets/win1.png': {e}")
        win_img = pygame.Surface((WINDOW_WIDTH, HEIGHT))
        win_img.fill(WHITE)
        text = font.render("¡Ganaste!", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, HEIGHT // 2))
        win_img.blit(text, text_rect)

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 5000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        window.blit(win_img, (0, 0))
        pygame.display.flip()
    return show_credits()

# Pantalla de Game Over
def game_over_screen():
    try:
        over_img = pygame.image.load("assets/Over1.png").convert()
        over_img = pygame.transform.scale(over_img, (WINDOW_WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading 'assets/Over1.png': {e}")
        over_img = pygame.Surface((WINDOW_WIDTH, HEIGHT))
        over_img.fill(WHITE)
        text = font.render("Game Over! Presiona ESC para volver al menú", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, HEIGHT // 2))
        over_img.blit(text, text_rect)

    while True:
        window.blit(over_img, (0, 0))
        text = font.render("Presiona ESC para volver al menú", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, HEIGHT - 50))
        window.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

# Pantalla de segunda oportunidad
def second_chance_screen(level, wait_time=2000):
    window.fill((135, 206, 235))
    text = font.render(f"SEGUNDA OPORTUNIDAD - NIVEL {level}", True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, HEIGHT // 2))
    window.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(wait_time)

# Pantalla de transición entre niveles
def next_level_screen(level, wait_time=2000):
    alpha = 0
    fade_surface = pygame.Surface((WINDOW_WIDTH, HEIGHT), pygame.SRCALPHA)
    while alpha < 255:
        window.fill((135, 206, 235))
        text = font.render(f"NEXT LEVEL {level}", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)
        fade_surface.fill((0, 0, 0, alpha))
        window.blit(fade_surface, (0, 0))
        pygame.display.flip()
        alpha += 5
        pygame.time.wait(20)
    pygame.time.wait(wait_time - 1000)

# Función del menú principal con nubes
def main_menu():
    buttons = {
        "Iniciar": pygame.Rect(WINDOW_WIDTH // 2 - 100, 200, 200, 50),
        "Guía": pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, 200, 50),
        "Créditos": pygame.Rect(WINDOW_WIDTH // 2 - 100, 400, 200, 50),
    }
    hover_color = (200, 200, 200)

    # Grupo de sprites para las nubes
    clouds = pygame.sprite.Group()
    # Crear 5 nubes iniciales
    for _ in range(5):
        cloud = Cloud()
        clouds.add(cloud)

    while True:
        window.blit(background_img, (0, 0))  # Fondo base
        clouds.update()  # Actualizar movimiento de las nubes
        clouds.draw(window)  # Dibujar nubes

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, button_rect in buttons.items():
                    if button_rect.collidepoint(mouse_pos):
                        return button_name

        for button_name, button_rect in buttons.items():
            color = hover_color if button_rect.collidepoint(mouse_pos) else GRAY
            pygame.draw.rect(window, color, button_rect)
            text = font.render(button_name, True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            window.blit(text, text_rect)

        pygame.display.flip()

# Función de la guía
def show_guide():
    try:
        guide_img = pygame.image.load("assets/fondoguia.png").convert()
        guide_img = pygame.transform.scale(guide_img, (WINDOW_WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading 'assets/fondoguia.png': {e}")
        guide_img = pygame.Surface((WINDOW_WIDTH, HEIGHT))
        guide_img.fill((100, 149, 237))
        text = font.render("Guía no disponible", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, HEIGHT // 2))
        guide_img.blit(text, text_rect)

    while True:
        window.blit(guide_img, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

# Función de créditos
def show_credits():
    try:
        credits_img = pygame.image.load("assets/Créditospipi.png").convert()
        credits_img = pygame.transform.scale(credits_img, (WINDOW_WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading 'assets/Créditospipi.png': {e}")
        credits_img = pygame.Surface((WINDOW_WIDTH, HEIGHT))
        credits_img.fill(WHITE)
        text = font.render("Créditos no disponibles", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, HEIGHT // 2))
        credits_img.blit(text, text_rect)

    while True:
        window.blit(credits_img, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

# Función del juego principal
def game_loop():
    current_level = 1
    clock = pygame.time.Clock()
    opportunities_used = [0] * 4

    while current_level <= 3:
        all_sprites, platforms, coins, enemies, player, explosions, coin_effects = create_level(current_level)
        if opportunities_used[current_level] == 1:
            player.lives = 1
        camera_x = player.rect.x - WINDOW_WIDTH // 2

        while True:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "quit"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Regresar al menú con ESC
                            return "menu"
                        if event.key == pygame.K_w:
                            player.jump()
                        if event.key == pygame.K_a:
                            player.vel_x = -5
                        if event.key == pygame.K_d:
                            player.vel_x = 5
                    if event.type == pygame.KEYUP:
                        if event.key in [pygame.K_a, pygame.K_d]:
                            player.vel_x = 0
            except Exception as e:
                print(f"Error al manejar eventos: {e}")
                continue

            game_over = player.update(platforms, enemies, explosions)
            for enemy in enemies:
                if enemy.follow_player:
                    enemy.update(player.rect.x, player.rect.y)  # Pasar tanto x como y del jugador
                else:
                    enemy.update()
            explosions.update()
            coin_effects.update()

            camera_x = player.rect.x - WINDOW_WIDTH // 2
            camera_x = max(0, min(camera_x, WORLD_WIDTH - WINDOW_WIDTH))

            if game_over == "game_over":
                opportunities_used[current_level] += 1
                if opportunities_used[current_level] == 1:
                    second_chance_screen(current_level)
                    break
                else:
                    result = game_over_screen()
                    return result

            player_center = (player.rect.centerx, player.rect.centery)
            for coin in coins:
                coin_center = (coin.rect.centerx, coin.rect.centery)
                distance = math.sqrt((player_center[0] - coin_center[0]) ** 2 + (player_center[1] - coin_center[1]) ** 2)
                if distance < coin.collect_radius:
                    effect = CoinEffect(coin.rect.centerx, coin.rect.centery)
                    coin_effects.add(effect)
                    coins.remove(coin)
                    all_sprites.remove(coin)
                    player.score += 10

            if len(coins) == 0:
                opportunities_used[current_level] = 0
                if current_level < 3:
                    current_level += 1
                    break  # Pasar al siguiente nivel sin transición
                else:
                    result = win_screen()
                    return result

            window.blit(background_img, (0, 0))
            for sprite in all_sprites:
                if sprite.rect.x - camera_x + sprite.rect.width >= 0 and sprite.rect.x - camera_x <= WINDOW_WIDTH:
                    window.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
            for enemy in enemies:
                if enemy.rect.x - camera_x + enemy.rect.width >= 0 and enemy.rect.x - camera_x <= WINDOW_WIDTH:
                    window.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))
            for effect in coin_effects:
                if effect.rect.x - camera_x + effect.rect.width >= 0 and effect.rect.x - camera_x <= WINDOW_WIDTH:
                    window.blit(effect.image, (effect.rect.x - camera_x, effect.rect.y))
            for explosion in explosions:
                if explosion.rect.x - camera_x + explosion.rect.width >= 0 and explosion.rect.x - camera_x <= WINDOW_WIDTH:
                    window.blit(explosion.image, (explosion.rect.x - camera_x, explosion.rect.y))

            score_surface = pygame.Surface((150, 40), pygame.SRCALPHA)
            score_surface.fill(TRANS_BLACK)
            window.blit(score_surface, (10, 10))
            score_text = font.render(f"Puntaje: {player.score}", True, WHITE)
            window.blit(score_text, (10, 10))

            level_surface = pygame.Surface((150, 40), pygame.SRCALPHA)
            level_surface.fill(TRANS_BLACK)
            level_rect = level_surface.get_rect(center=(WINDOW_WIDTH // 2, 20))
            window.blit(level_surface, level_rect)
            level_text = font.render(f"Nivel: {current_level}", True, WHITE)
            level_text_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, 20))
            window.blit(level_text, level_text_rect)

            for i in range(player.lives):
                window.blit(vida_img, (WINDOW_WIDTH - 50 - i * 50, 10))

            pygame.display.flip()
            clock.tick(60)

# Bucle principal del juego
try:
    running = True
    while running:
        action = main_menu()
        if action == "quit":
            running = False
        elif action == "Iniciar":
            result = game_loop()
            if result == "quit":
                running = False
            elif result == "menu":
                continue  # Regresar al menú principal
        elif action == "Guía":
            result = show_guide()
            if result == "quit":
                running = False
        elif action == "Créditos":
            result = show_credits()
            if result == "quit":
                running = False
except Exception as e:
    print(f"Error durante la ejecución del juego: {e}")
finally:
    print("Juego cerrado correctamente.")
    pygame.quit()