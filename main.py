import pygame, sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        # общая установка
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))  # создание экрана
        pygame.display.set_caption("Game")  # название экрана
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()
            self.screen.fill(WATER_COLOR)  # цвеет экрана
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
