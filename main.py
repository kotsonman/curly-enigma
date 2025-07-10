import pygame
import sys

# Классическая инициализация pygame
try:
    pygame.init()
    print("Pygame успешно инициализирован")
except pygame.error as e:
    print(f"Ошибка инициализации pygame: {e}")
    sys.exit(1)

# Настройки экрана
WIDTH, HEIGHT = 800, 600
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Тест pygame")
    print(f"Экран создан: {WIDTH}x{HEIGHT}")
except pygame.error as e:
    print(f"Ошибка создания экрана: {e}")
    pygame.quit()
    sys.exit(1)

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Часы для контроля FPS
clock = pygame.time.Clock()

# Основной цикл
running = True
while running:
    clock.tick(60)  # Ограничение до 60 FPS

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заливка экрана белым цветом
    screen.fill(WHITE)

    # Рисуем синий прямоугольник
    pygame.draw.rect(screen, BLUE, (350, 250, 100, 100))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы
pygame.quit()
sys.exit()