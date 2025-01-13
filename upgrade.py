import pygame
from settings import *


class Upgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UIFONT_SIZE)

        self.height = self.display_surface.get_size()[1] * 0.8
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
                if self.selection_index > 4:
                    self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.selection_index -= 1
                if self.selection_index < 0:
                    self.selection_index = 4
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].triger(self.player)

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
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


class Item:
    def __init__(self, L, t, w, h, index, font):
        self.rect = pygame.Rect(L, t, w, h)
        self.index = index
        self.font = font
        self.sound_upgrade = pygame.mixer.Sound("audio/heal.wav")
        self.sound_upgrade.set_volume(0.6)
        self.sound_lose = pygame.mixer.Sound("audio/hit.wav")
        self.sound_lose.set_volume(0.1)
        self.image_board = pygame.transform.scale(pygame.image.load("sprite/UI/upgrade_board.png").convert_alpha(),
                                                  (214, 640))

    def display_names(self, surface, name, cost, selected):
        if selected:
            color = TEXT_COLOR_SELECTED
        else:
            color = TEXT_COLOR

        # title
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        # cost
        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))

        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):

        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def triger(self, player):
        uprade_attribute = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[uprade_attribute] and player.stats[uprade_attribute] < \
                player.max_stats[uprade_attribute]:
            self.sound_upgrade.play()
            player.exp -= player.upgrade_cost[uprade_attribute]
            player.stats[uprade_attribute] *= 1.2
            player.upgrade_cost[uprade_attribute] *= 1.1
        else:
            self.sound_lose.play()
        if player.stats[uprade_attribute] > player.max_stats[uprade_attribute]:
            player.upgrade_cost[uprade_attribute] *= 0
            player.stats[uprade_attribute] = player.max_stats[uprade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            selected = True
        else:
            selected = False
        surface.blit(self.image_board, self.rect)
        self.display_names(surface, name, cost, selected)
        self.display_bar(surface, value, max_value, selected)

