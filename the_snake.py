from random import choice, randint

import abc

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

    def __init__(
            self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
            body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    @abc.abstractmethod
    def draw(self):
        """Отрисовка объекта"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def erase(self, last):
        """Затирание последней клетки"""
        last_rect = pygame.Rect(last, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Яблоко"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)

    def randomize_position(self):
        """Генерация случайной позиции"""
        self.position = (
            (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
            (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))

    def draw(self):
        """Отрисовка яблока"""
        super().draw()


class Snake(GameObject):
    """Змейка"""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.directions = [UP, DOWN, RIGHT, LEFT]
        self.direction = RIGHT
        self.last = None

    def update_direction(self, direction):
        """Обновление направления движения"""
        self.direction = direction

    def move(self):
        """Движение змейки"""
        x, y = self.get_head_position()
        a, b = self.direction
        new_head = (
            x + a * GRID_SIZE, y + b * GRID_SIZE)
        # столкновение c правым или левым краем
        if x % SCREEN_WIDTH == 0:
            if x == SCREEN_WIDTH:
                new_head = (GRID_SIZE, y)
            else:
                new_head = (SCREEN_WIDTH - GRID_SIZE, y)
        # столкновение c верхним или нижним краем
        if y % SCREEN_HEIGHT == 0:
            if y == SCREEN_HEIGHT:
                new_head = (x, GRID_SIZE)
            else:
                new_head = (x, SCREEN_HEIGHT - GRID_SIZE)

        # добавление новой головы
        self.positions.insert(0, new_head)
        # удаление последнего сегмента
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None
        # проверка на столкновение с собой
        if len(self.positions) > len(set(self.positions)):
            self.reset()

    def draw(self):
        """Отрисовка змейки"""
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # затирание последнего сегмента
        if self.last is not None:
            self.erase(self.last)

    def get_head_position(self):
        """Получение позиции головы"""
        return self.positions[0]

    def reset(self):
        """Обнуление позиции змейки и её длины"""
        self.direction = choice(self.directions)
        self.length = 1
        self.positions.insert(0, self.position)


def handle_keys(game_object):
    """Нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Игра"""
    # экземпляры классов.
    snake = Snake()
    apple = Apple()
    apple.randomize_position()
    print(apple.position)
    apple.draw()
    # цикл игры
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        snake.move()
        # Столкновение змейки и яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            apple.draw()
            print(apple.position)
        pygame.display.update()


if __name__ == '__main__':
    main()
