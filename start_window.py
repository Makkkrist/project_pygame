import pygame


class Start_window:
    def __init__(self, start_game):
        self.start_game = start_game
        self.display_surface = pygame.display.get_surface()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.start_game()

    def display(self):
        self.input()
        self.display_surface.blit(pygame.image.load("sprite/UI/Main_game.png").convert(), (0, 0))
