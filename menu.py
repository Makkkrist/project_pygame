import pygame
from settings import *


class Menu:
    def __init__(self, pause):
        self.display_surface = pygame.display.get_surface()
        self.flag_upgrade = False
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.names = ["улучшения персонажа", "выучить закленания", "выход из меню", "выход из игры"]
        self.font = pygame.font.Font(UI_FONT, UIFONT_SIZE)
        self.width = 300
        self.height = 50
        self.pause = pause
        self.flag_open_spell = False
        self.create_items()

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.selection_index += 1
                if self.selection_index > 3:
                    self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.selection_index -= 1
                if self.selection_index < 0:
                    self.selection_index = 3
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_RETURN]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.triger()

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(len(self.names))):
            top = 70 * index + 60

            left = 40
            item = Menu_Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def triger(self):
        if self.selection_index == 0:
            self.flag_upgrade = True

        elif self.selection_index == 1:
            self.flag_open_spell = True
        elif self.selection_index == 2:
            self.pause()
        elif self.selection_index == 3:
            exit()

    def display(self):
        self.input()
        self.selection_cooldown()
        for index, item in enumerate(self.item_list):
            name = self.names[index]
            item.display(self.display_surface, self.selection_index, name)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 100:
                self.can_move = True


class Menu_Item:
    def __init__(self, L, t, w, h, index, font):
        self.rect = pygame.Rect(L, t, w, h)
        self.index = index
        self.font = font
        self.sound_upgrade = pygame.mixer.Sound("audio/heal.wav")
        self.sound_upgrade.set_volume(0.6)
        self.sound_lose = pygame.mixer.Sound("audio/hit.wav")
        self.sound_lose.set_volume(0.1)

    def display_names(self, surface, name, selected):
        if selected:
            color = TEXT_COLOR_SELECTED
        else:
            color = TEXT_COLOR

        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))
        surface.blit(title_surf, title_rect)

    def display(self, surface, selection_num, name):
        if self.index == selection_num:
            selected = True
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            selected = False
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(surface, name, selected)
