from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# классы игры.
class GameObject:
    """Базовый класс"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка объекта"""
        pass


class Apple(GameObject):
    """Яблоко"""

    def __init__(self):
        self.position = (
            (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
            (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Генерация случайной позиции"""
        self.position = (
            (randint(0, GRID_WIDTH) * GRID_SIZE),
            (randint(0, GRID_HEIGHT) * GRID_SIZE))
        # если позиция яблока за пределами видимого поля
        if self.position[0] == 640 or self.position[1] == 480:
            self.position = (
                (randint(0, GRID_WIDTH) * GRID_SIZE),
                (randint(0, GRID_HEIGHT) * GRID_SIZE))

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = self.direction
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновление направления движения"""
        if self.next_direction != self.direction:
            self.direction = self.next_direction

    def move(self):
        """Движение змейки"""
        head_pos = self.get_head_position()
        new_head = (
            head_pos[0] + self.direction[0] * GRID_SIZE,
            head_pos[1] + self.direction[1] * GRID_SIZE)
        # столкновение c правым краем
        if head_pos[0] > SCREEN_WIDTH:
            new_head = (0, head_pos[1])
        # столкновение c левым краем
        elif head_pos[0] < 0:
            new_head = (SCREEN_WIDTH, head_pos[1])
        # столкновение c верхним краем
        if head_pos[1] < 0:
            new_head = (head_pos[0], SCREEN_HEIGHT)
        # столкновение c нижним краем
        elif head_pos[1] > SCREEN_HEIGHT:
            new_head = (head_pos[0], GRID_SIZE)
        # добавление новой головы
        self.positions.insert(0, new_head)
        # удаление последнего сегмента
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        # проверка на столкновение с собой
        if len(self.positions) > len(set(self.positions)):
            self.reset()

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    #  Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получение позиции головы"""
        return self.positions[0]

    def reset(self):
        """Обнуление позиции змейки и её длины"""
        for pos in self.positions:
            if self.last:
                last_rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        directions = [UP, DOWN, RIGHT, LEFT]
        self.direction = choice(directions)
        self.length = 1
        self.positions = [self.position]


def handle_keys(game_object):
    """Нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
                game_object.update_direction()
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
                game_object.update_direction()
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
                game_object.update_direction()
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
                game_object.update_direction()


def main():
    """Игра"""
    # экземпляры классов.
    running = True
    apple = Apple()
    apple.draw()
    snake = Snake()
    # цикл игры
    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        snake.move()
        # Столкновение змейки и яблока
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()
            for position in snake.positions[1:]:
                if position == apple.position:
                    apple.randomize_position()
            apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
