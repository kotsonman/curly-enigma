import pygame
import random
import sys

# Инициализация pygame
try:
    pygame.init()
    print("Pygame успешно инициализирован")
except pygame.error as e:
    print(f"Ошибка инициализации pygame: {e}")
    sys.exit(1)

# Настройки экрана
WIDTH, HEIGHT = 400, 600
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Doodle Jump")
    print(f"Экран создан: {WIDTH}x{HEIGHT}")
except pygame.error as e:
    print(f"Ошибка создания экрана: {e}")
    pygame.quit()
    sys.exit(1)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (135, 206, 235)

# Игровые параметры
GRAVITY = 0.8
JUMP_SPEED = -15
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLAYER_SIZE = 30
ENEMY_SIZE = 20

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.size = PLAYER_SIZE
        self.color = BLUE
        
    def update(self):
        # Применяем гравитацию
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Ограничиваем игрока в пределах экрана по горизонтали
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
            
    def jump(self):
        self.vel_y = JUMP_SPEED
        
    def draw(self, screen, camera_y):
        # Рисуем игрока относительно камеры
        pygame.draw.rect(screen, self.color, 
                        (self.x - self.size//2, self.y - camera_y - self.size//2, 
                         self.size, self.size))
        # Глаза
        pygame.draw.circle(screen, WHITE, 
                          (int(self.x - 5), int(self.y - camera_y - 5)), 3)
        pygame.draw.circle(screen, WHITE, 
                          (int(self.x + 5), int(self.y - camera_y - 5)), 3)
        pygame.draw.circle(screen, BLACK, 
                          (int(self.x - 5), int(self.y - camera_y - 5)), 1)
        pygame.draw.circle(screen, BLACK, 
                          (int(self.x + 5), int(self.y - camera_y - 5)), 1)

class Platform:
    def __init__(self, x, y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = GREEN
        
    def draw(self, screen, camera_y):
        pygame.draw.rect(screen, self.color, 
                        (self.x, self.y - camera_y, self.width, self.height))
        
    def check_collision(self, player):
        return (player.x + player.size//2 > self.x and 
                player.x - player.size//2 < self.x + self.width and
                player.y + player.size//2 > self.y and 
                player.y + player.size//2 < self.y + self.height + 10 and
                player.vel_y > 0)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = ENEMY_SIZE
        self.color = RED
        
    def draw(self, screen, camera_y):
        pygame.draw.rect(screen, self.color, 
                        (self.x - self.size//2, self.y - camera_y - self.size//2, 
                         self.size, self.size))
        
    def check_collision(self, player):
        return (player.x + player.size//2 > self.x - self.size//2 and 
                player.x - player.size//2 < self.x + self.size//2 and
                player.y + player.size//2 > self.y - self.size//2 and 
                player.y - player.size//2 < self.y + self.size//2)

class Game:
    def __init__(self):
        self.player = Player(WIDTH//2, HEIGHT - 100)
        self.platforms = []
        self.enemies = []
        self.camera_y = 0
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        
        # Создаем начальные платформы
        for i in range(10):
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            y = HEIGHT - 50 - i * 60
            self.platforms.append(Platform(x, y))
            
    def generate_platforms(self):
        # Удаляем платформы, которые ушли за экран
        self.platforms = [p for p in self.platforms if p.y - self.camera_y < HEIGHT + 100]
        
        # Добавляем новые платформы
        while len(self.platforms) < 10:
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            y = self.platforms[-1].y - random.randint(50, 80)
            self.platforms.append(Platform(x, y))
            
    def generate_enemies(self):
        # Удаляем врагов, которые ушли за экран
        self.enemies = [e for e in self.enemies if e.y - self.camera_y < HEIGHT + 50]
        
        # Добавляем новых врагов с вероятностью
        if random.random() < 0.02 and len(self.enemies) < 3:
            x = random.randint(ENEMY_SIZE//2, WIDTH - ENEMY_SIZE//2)
            y = self.camera_y + HEIGHT + 50
            self.enemies.append(Enemy(x, y))
            
    def update(self):
        if self.game_over:
            return
            
        # Обновляем игрока
        self.player.update()
        
        # Проверяем коллизии с платформами
        for platform in self.platforms:
            if platform.check_collision(self.player):
                self.player.jump()
                break
                
        # Проверяем коллизии с врагами
        for enemy in self.enemies:
            if enemy.check_collision(self.player):
                self.game_over = True
                break
                
        # Обновляем камеру
        if self.player.y - self.camera_y < HEIGHT//2:
            self.camera_y = self.player.y - HEIGHT//2
            
        # Обновляем счет
        self.score = max(self.score, int(self.camera_y // 10))
        
        # Генерируем новые платформы и врагов
        self.generate_platforms()
        self.generate_enemies()
        
        # Проверяем падение
        if self.player.y - self.camera_y > HEIGHT + 50:
            self.game_over = True
            
    def draw(self):
        # Фон
        screen.fill(SKY_BLUE)
        
        # Рисуем платформы
        for platform in self.platforms:
            platform.draw(screen, self.camera_y)
            
        # Рисуем врагов
        for enemy in self.enemies:
            enemy.draw(screen, self.camera_y)
            
        # Рисуем игрока
        self.player.draw(screen, self.camera_y)
        
        # Рисуем счет
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Рисуем сообщение о конце игры
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.font.render("Press R to restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))
            
    def restart(self):
        self.__init__()

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game.restart()
                    
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game.player.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game.player.x += 5
            
        game.update()
        game.draw()
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 