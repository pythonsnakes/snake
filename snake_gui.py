import sched
import time
from threading import Thread
from tkinter import *

from snake_model import Point, Direction, GameModel, GameResult


class SnakeGame:
    SPEED = 0.15
    SEG_SIZE = 20
    SEG_NUMBER = 40
    PIXEL_SIZE = SEG_SIZE * SEG_NUMBER
    SNAKE_COLOR1 = "yellow"
    SNAKE_COLOR2 = "blue"

    BG_COLOR = "#003300"

    def __init__(self, start):
        self.game_model = GameModel(SnakeGame.SEG_NUMBER)
        root = Tk()
        root.title("Cool Snake")
        self.canvas = Canvas(root, width=SnakeGame.PIXEL_SIZE,
                             height=SnakeGame.PIXEL_SIZE,
                             bg=SnakeGame.BG_COLOR)
        self.canvas.pack()
        self.canvas.focus_set()
        self.draw_snake(self.game_model.first_snake.body,
                        SnakeGame.SNAKE_COLOR1)
        self.draw_snake(self.game_model.second_snake.body,
                        SnakeGame.SNAKE_COLOR2)
        self.draw_grid_of_field()
        self.game_model.drop_food()
        self.draw_food(self.game_model.food)
        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.canvas.bind('<Key>', self.change_direction)
        self.run_snake_moving_thread()

        root.mainloop()

    def run_snake_moving_thread(self):
        thread = Thread(target=self.play_game)
        thread.start()

    def draw_food(self, points):
        for p in points:
            x = p.x * SnakeGame.SEG_SIZE
            y = p.y * SnakeGame.SEG_SIZE

            self.canvas.create_oval(x, y, x + SnakeGame.SEG_SIZE,
                                    y + SnakeGame.SEG_SIZE,
                                    fill="red",tag = "f")

    def draw_square(self, point, color):
        x = point.x * SnakeGame.SEG_SIZE
        y = point.y * SnakeGame.SEG_SIZE
        self.canvas.create_rectangle(x, y,
                                           x + SnakeGame.SEG_SIZE - 1,
                                           y + SnakeGame.SEG_SIZE - 1,
                                           fill=color, tag = "seg")

    def draw_snake(self, snake_body, color):
        for p in snake_body:
            self.draw_square(p, color)

    def draw_grid_of_field(self):
        for i in range(0, SnakeGame.SEG_NUMBER):
            self.canvas.create_line(0, i * SnakeGame.SEG_SIZE,
                                    SnakeGame.PIXEL_SIZE,
                                    i * SnakeGame.SEG_SIZE, fill="black")
            self.canvas.create_line(i * SnakeGame.SEG_SIZE, 0,
                                    i * SnakeGame.SEG_SIZE,
                                    SnakeGame.PIXEL_SIZE, fill="black")

    def change_direction(self, event):
        if event.keysym == "Left":
            self.game_model.first_snake.set_dir(Direction.LEFT)
        elif event.keysym == "Right":
            self.game_model.first_snake.set_dir(Direction.RIGHT)
        elif event.keysym == "Up":
            self.game_model.first_snake.set_dir(Direction.UP)
        elif event.keysym == "Down":
            self.game_model.first_snake.set_dir(Direction.DOWN)

        if event.keysym == "a":
            self.game_model.second_snake.set_dir(Direction.LEFT)
        elif event.keysym == "d":
            self.game_model.second_snake.set_dir(Direction.RIGHT)
        elif event.keysym == "w":
            self.game_model.second_snake.set_dir(Direction.UP)
        elif event.keysym == "s":
            self.game_model.second_snake.set_dir(Direction.DOWN)

    def draw_game_result(self, game_result):
        if game_result == GameResult.SNAKE1_WIN:
            text = str(self.SNAKE_COLOR1) + " snake win! "
        if game_result == GameResult.SNAKE2_WIN:
            text = str(self.SNAKE_COLOR2) + " snake win! "
        if game_result == GameResult.DRAW:
            text = "DRAW"
        self.canvas.create_text(self.PIXEL_SIZE / 2,
                                self.PIXEL_SIZE / 2,
                                text=text, font="Arial 40",
                                fill="red")

    def process_game_step(self):
        self.game_model.check_bump_into_self()
        self.game_model.check_collision()
        if self.game_model.game_result != None:
            self.draw_game_result(self.game_model.game_result)
            return
        snake1_is_crashed = False
        snake2_is_crashed = False
        if self.game_model.first_snake.current_dir != None:
            snake1_is_crashed = not self.game_model.first_snake.move()
        if self.game_model.second_snake.current_dir != None:
            snake2_is_crashed = not self.game_model.second_snake.move()
        if snake1_is_crashed and snake2_is_crashed:
            self.game_model.game_result = GameResult.DRAW
            self.draw_game_result(self.game_model.game_result)
            return
        elif snake1_is_crashed:
            self.game_model.game_result = GameResult.SNAKE2_WIN
            self.draw_game_result(self.game_model.game_result)
            return
        elif snake2_is_crashed:
            self.game_model.game_result = GameResult.SNAKE1_WIN
            self.draw_game_result(self.game_model.game_result)
            return
        self.game_model.check_eaten_food()
        self.game_model.drop_food()
        self.canvas.delete("seg")
        self.canvas.delete("f")
        self.draw_snake(self.game_model.first_snake.body,
                        SnakeGame.SNAKE_COLOR1)
        self.draw_snake(self.game_model.second_snake.body,
                        SnakeGame.SNAKE_COLOR2)
        self.draw_food(self.game_model.food)

    def play_game(self):
        while self.game_model.game_result == None:
            self.scheduler.enter(SnakeGame.SPEED, 1, self.process_game_step)
            self.scheduler.run()


def main():
    start = Point(5, 5)
    game1 = SnakeGame(start)


main()
