import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from UI import UI
from enemy import Enemy
from paricles import AnimationPlayer
from Magic import MagicPlayer
from upgrade import Upgrade
from start_window import Start_window
from menu import Menu
from open_spell import Open_spell


class Level:
    def __init__(self):
        # взятие экрана поверхности
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # группа спрайтоф установка
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.current_attack = None

        # спрайты атак
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # установка спрайтов
        self.create_map()

        # интерфейс польвателя
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.start_window = Start_window(self.start_Game)
        self.menu = Menu(self.toggle_menu)
        self.open_spell = Open_spell(self.player)

        # частицы
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        self.flag_death_player = False
        self.flag_start_game = True

    def create_map(self):
        layouts = {"boundary": import_cvs_layout("map/map_FloorBlocks.csv"),
                   "grass": import_cvs_layout("map/map_Grass.csv"),
                   "entities": import_cvs_layout("map/map_Entities.csv")}
        graphics = {
            "grass": import_folder("sprite/graphics/grass"),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            if col == "395":
                                Tile((x, y), [self.visible_sprites, self.obstacles_sprites], "invisible",
                                     pygame.image.load("sprite/lelel/wall.png").convert_alpha())

                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites],
                                 "grass", random_grass_image)
                        if style == "entities":
                            if col == "394":
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacles_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic,
                                                     self.death_player)
                            else:
                                # условия чтобы понять что за моб
                                if col == "390":
                                    monster_name = "bamboo"
                                elif col == "391":
                                    monster_name = "spirit"
                                elif col == "392":
                                    monster_name = "raccoon"
                                else:
                                    monster_name = "squid"
                                Enemy(monster_name,
                                      (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacles_sprites,
                                      self.damage_player,
                                      self.triger_death_particles,
                                      self.add_exp,
                                      )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):  # функция для создания магии
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == "flame":
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        if style == "boost_speed":
            self.magic_player.boost_speed(self.player, cost, [self.visible_sprites])
        if style == "inferno":
            self.magic_player.inferno(self.player, cost, [self.visible_sprites, self.attack_sprites])
        if style == "fire":
            self.magic_player.fire(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):  # логика атаки перснажа
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":  # условия, чтобы понять ,что он ударяет
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)

                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, self.visible_sprites)
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):  # функция для вычита хп
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def triger_death_particles(self, pos, particle_type):  # функция создющая частицы при смерти моба
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount
        self.player.exp_end += amount
        self.player.count_kills += 1
        if self.player.count_kills == 3:
            self.player.hitbox.topleft = (128, 3328)
            self.player.rect.topleft = (128, 3328)
            Enemy('raccoon',
                  (128 * 2, 3328),
                  [self.visible_sprites, self.attackable_sprites],
                  self.obstacles_sprites,
                  self.damage_player,
                  self.triger_death_particles,
                  self.add_exp,
                  )
            Enemy('raccoon',
                  (128 * 2, 3328 + 64 * 3),
                  [self.visible_sprites, self.attackable_sprites],
                  self.obstacles_sprites,
                  self.damage_player,
                  self.triger_death_particles,
                  self.add_exp,
                  )

    def toggle_menu(self):
        self.game_paused = not self.game_paused
        self.menu.flag_upgrade = False
        self.menu.flag_open_spell = False

    def death_player(self):
        font = pygame.font.Font(UI_FONT, UIFONT_SIZE)
        string_exp = f"количество опыта:{self.player.exp_end}"
        string_kills = f"количество убийств:{self.player.count_kills}"
        self.text_surf_exp = font.render(string_exp, False, TEXT_COLOR)
        self.text_rect_exp = self.text_surf_exp.get_rect(topleft=(333, 106))
        self.text_surf_kills = font.render(string_kills, False, TEXT_COLOR)
        self.text_rect_kills = self.text_surf_kills.get_rect(topleft=(333, 136))
        self.flag_death_player = True
        self.game_paused = True

    def start_Game(self):
        self.flag_start_game = False

    def run(self):
        if self.flag_start_game:
            self.start_window.display()
        else:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
            if self.game_paused:
                if self.flag_death_player:
                    self.display_surface.blit(pygame.image.load("sprite/UI/game_over.png").convert(), (0, 0))
                    self.display_surface.blit(self.text_surf_exp, self.text_rect_exp)
                    self.display_surface.blit(self.text_surf_kills, self.text_rect_kills)
                else:
                    if self.menu.flag_upgrade:
                        self.upgrade.display()
                    elif self.menu.flag_open_spell:
                        self.open_spell.display()
                    else:
                        self.menu.display()

            else:
                # рисование и обновление  игры
                self.visible_sprites.update()
                self.visible_sprites.enemy_update(self.player)
                self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # создание уровня
        self.floor_surf = pygame.image.load("sprite/lelel/level.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and
                         sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
