import pygame
from settings import *
from support import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, death_player):
        super().__init__(groups)
        self.image = pygame.image.load("sprite/graphics/player/left/left_0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["player"])

        # установка графики
        self.import_player_assets()
        self.status = "down"

        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 4, "speed": 6}
        self.max_stats = {"health": 300, "energy": 140, "attack": 20, "magic": 10, "speed": 12}
        self.upgrade_cost = {"health": 100, "energy": 100, "attack": 100, "magic": 100, "speed": 100}
        self.health = self.stats["health"]

        self.energy = self.stats["energy"]
        self.exp = 0
        self.exp_end = 0
        self.count_kills = 0

        # магия
        self.magic_index = 0
        self.list_spell = [list(magic_data.keys())[0]]
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.create_magic = create_magic

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # оружие
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.weapon_duration = weapon_data[self.weapon]["cooldown"] * 15
        self.time_can_attack = None
        self.can_attack = True

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.death_player = death_player

        # импотр звуков
        self.weapon_attack_sound = pygame.mixer.Sound("audio/sword.wav")
        self.weapon_attack_sound.set_volume(0.2)
        self.sound_swith = pygame.mixer.Sound("audio/sword.wav")
        self.sound_swith.set_volume(0.03)

        # баф скорости
        self.flag_boost_speed = False
        self.time_boost_speed = None
        self.duration_boost_speed = 3000
        self.add_speed = 1 * self.stats["magic"]

    def import_player_assets(self):
        character_path = "sprite/graphics/player/"
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": [],
                           "up_attack": [], "down_attack": [], "left_attack": [], "right_attack": []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0
            # ввод атаки
            if keys[pygame.K_SPACE]:
                if self.can_attack:
                    self.can_attack = False
                    self.time_can_attack = pygame.time.get_ticks() - self.attack_cooldown + weapon_data[self.weapon][
                        "cooldown"]
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.create_attack()
                    self.weapon_attack_sound.play()
            # ввод магии
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = self.list_spell[self.magic_index]
                strength = magic_data[style]["strength"]
                cost = magic_data[style]["cost"]
                self.add_speed = 1 * self.stats["magic"]
                self.create_magic(style, strength, cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % 5
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                self.sound_swith.play()

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                self.magic_index = (self.magic_index + 1) % len(self.list_spell)
                self.magic = list(self.list_spell)[self.magic_index]
                self.sound_swith.play()

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if "idle" not in self.status and "attack" not in self.status:
                self.status = self.status + "_idle"
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if "attack" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
        if self.flag_boost_speed:
            if current_time - self.time_boost_speed >= self.duration_boost_speed:
                self.flag_boost_speed = False
        if not self.can_attack:
            if current_time - self.time_can_attack >= self.weapon_duration:
                self.can_attack = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats["magic"]
        spell_damage = magic_data[self.magic]["strength"]
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def check_death(self):
        if self.health <= 0:
            self.death_player()

    def update(self):
        self.check_death()
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"] + self.add_speed * self.flag_boost_speed)
        self.energy_recovery()
