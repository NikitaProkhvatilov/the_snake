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


# Тут опишите все классы игры.
class GameObject:
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        pass

class Apple(GameObject):
    def randomize_position(self):
        return (
            (randint(0, GRID_HEIGHT) * GRID_SIZE),
            (randint(0, GRID_WIDTH) * GRID_SIZE))

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = self.direction
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        if self.next_direction != self.direction:
            self.direction = self.next_direction
            
    def move(self):
        """Движение змейки"""
        head_pos = self.get_head_position()
        if self.direction == RIGHT:
            new_head = (head_pos[0] + GRID_SIZE, head_pos[1])
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
        elif self.direction == LEFT:
            new_head = (head_pos[0] - GRID_SIZE, head_pos[1])
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
        elif self.direction == UP:
            new_head = (head_pos[0], head_pos[1] - GRID_SIZE)
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
        elif self.direction == DOWN:
            new_head = (head_pos[0], head_pos[1] + GRID_SIZE)
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

        """Столкновение змейки с краем экрана"""
        # столкновение c левым краем
        if head_pos[0] == 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, head_pos[1])
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
        # столкновение c правым краем
        elif head_pos[0] == SCREEN_WIDTH:
            new_head = (GRID_SIZE, head_pos[1])
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
        # столкновение c верхним краем
        elif head_pos[1] == 0:
            new_head = (head_pos[0], SCREEN_HEIGHT - GRID_SIZE)
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
        # столкновение c нижним краем
        elif head_pos[1] == SCREEN_HEIGHT:
            new_head = (head_pos[0], GRID_SIZE)
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
        
            

    def draw(self):
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
        return self.positions[0]

    def reset(self):
        pass

def handle_keys(game_object):
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
    # Тут нужно создать экземпляры классов.
    running = True
    apple = Apple()
    apple.draw()
    snake = Snake()
    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        snake.move()
        pygame.display.update()

        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()


# Метод draw класса Apple
#  def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
