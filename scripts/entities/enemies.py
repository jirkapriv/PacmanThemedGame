import random
from pathlib import Path

import pygame

from ..config.config import MAP_SCALE
from .player import Player

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENEMY_IMAGES = {
    "cervenak": BASE_DIR / "images" / "cervenak.png",
    "ruzovak": BASE_DIR / "images" / "ruzovak.png",
    "oranzovak": BASE_DIR / "images" / "oranzovak.png",
    "azurak": BASE_DIR / "images" / "azurak.png",
}


class Enemy(Player):
    """
    Enemy class that inherits from Player class
    """

    can_kill = True

    def __init__(
        self,
        game,
        map_obj,
        x,
        y,
        color_name,
        speed=1,
        vision_tiles=4,
    ):
        super().__init__(
            game, map_obj, x, y, action=random.choice(["left", "right", "up", "down"])
        )

        self.speed = speed
        self.vision_tiles = vision_tiles
        self.color_name = color_name
        self.change_dir_delay = 500
        self.last_dir_change = pygame.time.get_ticks()
        self.prepare_image()

    def render(self) -> None:
        self.game.screen.blit(self.image, self.player_rect)

    def prepare_image(self) -> None:
        """
        prepares images by loading, scaling, removing background
        """
        path = ENEMY_IMAGES[self.color_name]
        self.image = pygame.image.load(path)

        self.image = pygame.transform.scale(
            self.image, (self.tile_size, self.tile_size)
        )
        self.image.set_colorkey((255, 255, 255))
        self.player_rect = self.image.get_rect(topleft=(self.x, self.y))

    def can_see_player(self) -> bool:
        """
        check if a player is close enough to be seen by enemy
            todoo check in d circle mby
        """
        p_x, p_y = self.game.player.player_rect.center
        e_x, e_y = self.player_rect.center

        vision_len = self.tile_size * self.vision_tiles

        return abs(p_x - e_x) <= vision_len and abs(p_y - e_y) <= vision_len

    def chase_player(self) -> None:
        """
        movement choice by larger distance on x and y axis
        """
        p_x, p_y = self.game.player.player_rect.center
        e_x, e_y = self.player_rect.center

        d_x = p_x - e_x
        d_y = p_y - e_y

        if abs(d_x) > abs(d_y):
            self.next_action = "right" if d_x > 0 else "left"
        else:
            self.next_action = "down" if d_y > 0 else "up"

    def random_move(self) -> None:
        """
        rndom movement choice
        """
        directions = ["left", "right", "up", "down"]
        random.shuffle(directions)
        for d in directions:
            if self.map.can_move(self.player_rect, d):
                self.next_action = d
                return

    def update(self) -> None:
        now = pygame.time.get_ticks()

        if Enemy.can_kill and self.can_see_player():
            self.chase_player()
        elif now - self.last_dir_change > self.change_dir_delay:
            self.random_move()
            self.last_dir_change = now

        old_pos = self.player_rect.topleft
        self.move_player()

        tile_size = 8 * MAP_SCALE
        tile_x = self.player_rect.centerx // tile_size
        tile_y = self.player_rect.centery // tile_size

        if self.map.is_wall_tile(tile_x, tile_y):
            self.player_rect.topleft = old_pos
            self.random_move()
