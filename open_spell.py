import pygame
from settings import *


class Open_spell:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(magic_data) - 1
        self.attribute_names = list(magic_data.keys())[1:]
        self.font = pygame.font.Font(UI_FONT, UIFONT_SIZE)

        self.height = self.display_surface.get_size()[1] * 0.2
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # выбор
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.selection_index += 1
                if self.selection_index > 3:
                    self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.selection_index -= 1
                if self.selection_index < 0:
                    self.selection_index = 3
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].triger(self.player, self.attribute_names[self.selection_index])

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 100:
                self.can_move = True

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_nr)):
            top = self.display_surface.get_size()[1] * 0.1
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_nr
            left = (item * increment) + (increment - self.width) // 2
            cost = magic_data[self.attribute_names[index]]["exp"]
            item = Item(left, top, self.width, self.height, index, self.font, cost)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]

            item.display(self.display_surface, self.selection_index, name)


class Item:
    def __init__(self, L, t, w, h, index, font, cost):
        self.rect = pygame.Rect(L, t, w, h)
        self.index = index
        self.cost = cost
        self.font = font
        self.sound_upgrade = pygame.mixer.Sound("audio/heal.wav")
        self.sound_upgrade.set_volume(0.6)
        self.sound_lose = pygame.mixer.Sound("audio/hit.wav")
        self.sound_lose.set_volume(0.1)
        self.flag_open = False
        self.image_board = pygame.transform.scale(pygame.image.load("sprite/UI/opengame_board.png").convert_alpha(),
                                                  (200, 200))

    def display_names(self, surface, name, selected):
        if selected:
            color = TEXT_COLOR_SELECTED
        else:
            color = TEXT_COLOR

        # title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 30))

        # cost
        cost_surf = self.font.render(f'{int(self.cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom + pygame.math.Vector2(0, 10))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def triger(self, player, name):
        if not self.flag_open and player.exp >= self.cost:
            player.list_spell.append(name)
            player.exp -= self.cost
            self.cost = 0
            self.flag_open = True

    def display(self, surface, selection_num, name):
        if self.index == selection_num:
            selected = True
        else:
            selected = False
        surface.blit(self.image_board, self.rect)
        self.display_names(surface, name, selected)
