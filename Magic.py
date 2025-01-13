import pygame
from settings import *
from random import randint


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            "heal": pygame.mixer.Sound("audio/heal.wav"),
            "flame": pygame.mixer.Sound("audio/Fire.wav"),
            "lose": pygame.mixer.Sound("audio/hit.wav")

        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost and player.health < player.stats["health"]:
            player.health += strength
            player.energy -= cost
            player.health = min(player.health, player.stats["health"])
            self.animation_player.create_particles("aura", player.rect.center, groups)
            self.sounds["heal"].play()
        else:
            self.sounds["lose"].play()

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            if player.status.split("_")[0] == "right":
                dirction = pygame.math.Vector2(1, 0)
            elif player.status.split("_")[0] == "left":
                dirction = pygame.math.Vector2(-1, 0)
            elif player.status.split("_")[0] == "down":
                dirction = pygame.math.Vector2(0, 1)
            else:
                dirction = pygame.math.Vector2(0, -1)
            for i in range(1, 6):
                if dirction.x:
                    offset_x = (dirction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles("flame", (x, y), groups)
                else:
                    offset_y = (dirction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles("flame", (x, y), groups)
        else:
            self.sounds["lose"].play()

    def boost_speed(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            player.flag_boost_speed = True
            player.time_boost_speed = pygame.time.get_ticks()
            self.animation_player.create_particles("aura", player.rect.center, groups)
            self.sounds["heal"].play()
        else:
            self.sounds["lose"].play()

    def fire(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            if player.status.split("_")[0] == "right":
                dirction = pygame.math.Vector2(1, 0)
            elif player.status.split("_")[0] == "left":
                dirction = pygame.math.Vector2(-1, 0)
            elif player.status.split("_")[0] == "down":
                dirction = pygame.math.Vector2(0, 1)
            else:
                dirction = pygame.math.Vector2(0, -1)

            if dirction.x:
                offset_x = dirction.x * TILESIZE
                x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles("flame", (x, y), groups)
            else:
                offset_y = dirction.y * TILESIZE
                x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles("flame", (x, y), groups)
        else:
            self.sounds["lose"].play()

    def inferno(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            for i in range(1, 3):
                x = player.rect.centerx + i * TILESIZE + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles("flame", (x, y), groups)
                self.animation_player.create_particles("flame", (x, y - TILESIZE), groups)
                self.animation_player.create_particles("flame", (x, y + TILESIZE), groups)
                x = player.rect.centerx - i * TILESIZE + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles("flame", (x, y), groups)
                self.animation_player.create_particles("flame", (x, y - TILESIZE), groups)
                self.animation_player.create_particles("flame", (x, y + TILESIZE), groups)
                x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                y = player.rect.centery + i * TILESIZE + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles("flame", (x, y), groups)
                self.animation_player.create_particles("flame", (x - TILESIZE, y), groups)
                self.animation_player.create_particles("flame", (x + TILESIZE, y), groups)
                y = player.rect.centery - i * TILESIZE + randint(-TILESIZE // 3, TILESIZE // 3)
                self.animation_player.create_particles("flame", (x, y - TILESIZE), groups)
                self.animation_player.create_particles("flame", (x - TILESIZE, y), groups)
                self.animation_player.create_particles("flame", (x + TILESIZE, y), groups)
