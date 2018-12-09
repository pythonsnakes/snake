import copy
import random
from enum import Enum


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            if self.x == other.x and self.y == other.y:
                return True
        return False

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        if isinstance(other, Direction):
            return Point(self.x - other.value.x, self.y - other.value.y)
        raise TypeError("Other's type must be Point or Direction")

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, Direction):
            return Point(self.x + other.value.x, self.y + other.value.y)
        raise TypeError("Other's type must be Point or Direction")


class GameModel:
    def __init__(self, size):
        self.game_over = False
        self.size = size
        self.first_snake = SnakeModel(Point(1, 1), size)
        self.second_snake = SnakeModel(Point(1, 18), size)
        self.food = None
        self.food = []
        self.generate_food()
        self.game_result = None

    def check_collision(self):
        head1 = self.first_snake.body[0]
        head2 = self.second_snake.body[0]
        if self.first_snake.current_dir == None:
            head_1_new_position = head1
        else:
            head_1_new_position = head1 + self.first_snake.current_dir
        if self.second_snake.current_dir == None:
            head_2_new_position = head2
        else:
            head_2_new_position = head2 + self.second_snake.current_dir
        if head_1_new_position == head2 and head_2_new_position == head1:
            snake1_is_dead = not self.first_snake.shrink()
            self.first_snake.is_collided = True
            snake2_is_dead = not self.second_snake.shrink()
            self.second_snake.is_collided = True
            if snake1_is_dead and snake2_is_dead:
                self.game_result = GameResult.DRAW
            elif snake1_is_dead:
                self.game_result = GameResult.SNAKE2_WIN
            elif snake2_is_dead:
                self.game_result = GameResult.SNAKE1_WIN
        elif head_1_new_position in self.second_snake.body:
            self.first_snake.is_collided = True
            if self.first_snake.shrink() == False:
                self.game_result = GameResult.SNAKE2_WIN
        elif head_2_new_position in self.first_snake.body:
            self.second_snake.is_collided = True
            if self.second_snake.shrink() == False:
                self.game_result = GameResult.SNAKE1_WIN

    def generate_food(self):
        point = self.get_random_point()
        while point in self.first_snake.body \
                or point in self.second_snake.body \
                or point in self.food:
            point = self.get_random_point()
        self.food.append(point)

    def drop_food(self):
        if len(self.food) == 0:
            self.generate_food()
            self.generate_food()
        if len(self.food) == 1:
            self.generate_food()

    def get_random_point(self):
        x = random.randint(0, self.size-1)
        y = random.randint(0, self.size-1)
        return Point(x, y)

    def check_eaten_food(self):
        if self.first_snake.body[0] in self.food:
            self.first_snake.grow()
            self.food.remove(self.first_snake.body[0])

        if self.second_snake.body[0] in self.food:
            self.second_snake.grow()
            self.food.remove(self.second_snake.body[0])


class SnakeModel:
    def __init__(self, head, size, body=None):
        self.size = size
        self.body = [head]
        self.last_dir = None
        self.current_dir = None
        self.is_collided = False
        if body:
            self.body.extend(body)
            delta_x = head.x - self.body[1].x
            delta_y = head.y - self.body[1].y
            self.last_dir = Direction(Point(delta_x, delta_y))

    def add_segment(self, point):
        self.body.append(point)

    def grow(self):
        dir = self.last_dir
        tall = self.body[-1]
        if len(self.body) == 1:
            new_tall = Point(tall.x - dir.value.x, tall.y - dir.value.y)
            self.body.append(new_tall)
        else:
            prev_tall = self.body[-2]
            delta_x = prev_tall.x - tall.x
            delta_y = prev_tall.y - tall.y
            # сделать проверку на то, упирается ли змейка в стенку при добавлении
            new_tall = Point(tall.x - delta_x, tall.y - delta_y)
            self.body.append(new_tall)

    def shrink(self):
        if len(self.body) == 1:
            return False
        del self.body[-1]
        return True

    def move(self):
        if self.is_collided == True:
            self.is_collided = False
            return True
        head = self.body[0]
        prev_seg = copy.deepcopy(head)
        head.x += self.current_dir.value.x
        head.y += self.current_dir.value.y
        if head.x < 0 or head.x >= self.size \
                or head.y < 0 or head.y >= self.size:
            return False
        for i in range(1, len(self.body)):
            p = self.body[i]
            self.body[i] = prev_seg
            prev_seg = p
        self.last_dir = self.current_dir
        return True

    def set_dir(self, dir):
        if not dir.is_opposite(self.current_dir):
            self.current_dir = dir


class Direction(Enum):
    RIGHT = Point(1, 0)
    LEFT = Point(-1, 0)
    UP = Point(0, -1)
    DOWN = Point(0, 1)

    def is_opposite(self, dir):
        if dir == Direction.RIGHT and self == Direction.LEFT:
            return True
        if dir == Direction.LEFT and self == Direction.RIGHT:
            return True
        if dir == Direction.DOWN and self == Direction.UP:
            return True
        if dir == Direction.UP and self == Direction.DOWN:
            return True
        return False


class GameResult(Enum):
    DRAW = 0
    SNAKE1_WIN = 1
    SNAKE2_WIN = 2
