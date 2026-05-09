from pathlib import Path
from typing import Tuple

import pygame

from ..config.config import HEIGHT, MAP_SCALE, PLAYER_SCALE, WIDTH

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PLAYER_PATH1 = BASE_DIR / "images" / "pacman1_fow.png"
PLAYER_PATH2 = BASE_DIR / "images" / "pacman2_fow.png"


class Player:
    """
    Class for The player (Pac-MAn)
        animations, collisions, movement
    """

    def __init__(
        self, game, map_obj, x=WIDTH // 2, y=HEIGHT // 2, action="right", speed=4
    ):
        self.game = game
        self.map = map_obj
        self.action = action
        self.next_action: str | None = None
        self.tile_size = 8 * MAP_SCALE
        self.x = x
        self.y = y
        self.player_images = self.prepare_player_image()
        self.player_rect = self.player_images[0][0].get_rect()
        self.player_rect.topleft = (self.x, self.y)
        self.speed = speed

    def prepare_player_image(self):
        player = pygame.image.load(str(PLAYER_PATH1)).convert()
        player2 = pygame.image.load(str(PLAYER_PATH2)).convert()
        player.set_colorkey((255, 255, 255))
        player2.set_colorkey((255, 255, 255))

        player = pygame.transform.scale(
            player,
            (player.get_width() * PLAYER_SCALE, player.get_height() * PLAYER_SCALE),
        )
        player2 = pygame.transform.scale(
            player2,
            (player2.get_width() * PLAYER_SCALE, player2.get_height() * PLAYER_SCALE),
        )

        return [
            (player, player2),
            (
                pygame.transform.flip(player, True, False),
                pygame.transform.flip(player2, True, False),
            ),
            (pygame.transform.rotate(player, 90), pygame.transform.rotate(player2, 90)),
            (
                pygame.transform.rotate(player, 270),
                pygame.transform.rotate(player2, 270),
            ),
        ]

    @staticmethod
    def animate(images) -> pygame.Surface:
        """
        chooses player image by time
        """
        time = pygame.time.get_ticks()
        animation_duration = 650
        frame_count = len(images)
        frame_duration = animation_duration / frame_count
        frame = int((time % animation_duration) // frame_duration)
        return images[frame]

    def get_next_tile(self, direction=None) -> Tuple[int, int]:
        """
        computes tile coordinates in the given direction
        """
        if direction is None:
            direction = self.action
        x, y = self.x, self.y
        if direction == "left":
            x = (self.player_rect.left - 1) // self.tile_size
            y = self.player_rect.centery // self.tile_size
        elif direction == "right":
            x = (self.player_rect.right + 1) // self.tile_size
            y = self.player_rect.centery // self.tile_size
        elif direction == "up":
            x = self.player_rect.centerx // self.tile_size
            y = (self.player_rect.top - 1) // self.tile_size
        elif direction == "down":
            x = self.player_rect.centerx // self.tile_size
            y = (self.player_rect.bottom + 1) // self.tile_size
        return x, y

    def move_player(self) -> None:
        """
        Handles plaeyr movement
            implementing action buffer and movement
        """
        if self.next_action:
            if (
                self.player_rect.centerx % self.tile_size == self.tile_size // 2
                and self.player_rect.centery % self.tile_size == self.tile_size // 2
            ):
                tile_x, tile_y = self.get_next_tile(self.next_action)
                if not self.map.is_wall_tile(tile_x, tile_y):
                    self.action = self.next_action
                    self.next_action = None

        tile_x, tile_y = self.get_next_tile(self.action)
        if not self.map.is_wall_tile(tile_x, tile_y):
            if self.action == "left":
                self.player_rect.x -= self.speed
            elif self.action == "right":
                self.player_rect.x += self.speed
            elif self.action == "up":
                self.player_rect.y -= self.speed
            elif self.action == "down":
                self.player_rect.y += self.speed
            
        
        
        # Tunel implementation
        tile_x = self.player_rect.centerx // self.tile_size
        
        if self.action == "left" and tile_x == -1:
            self.player_rect.centerx = WIDTH
        elif self.action == "right" and tile_x == 21: # Game has 20 tiles in width
            self.player_rect.centerx = 0
                
        

        # centers player into the middle of a tile
        if self.action in ("left", "right"):
            self.player_rect.centery = (
                self.player_rect.centery // self.tile_size
            ) * self.tile_size + self.tile_size // 2
        else:
            self.player_rect.centerx = (
                self.player_rect.centerx // self.tile_size
            ) * self.tile_size + self.tile_size // 2

    def render_player(self) -> None:
        """
        decides w image to render
        """
        screen = self.game.screen
        if self.action == "left":
            img = self.player_images[1]
        elif self.action == "up":
            img = self.player_images[2]
        elif self.action == "right":
            img = self.player_images[0]
        elif self.action == "down":
            img = self.player_images[3]
        else:
            img = self.player_images[0]
        screen.blit(self.animate(img), self.player_rect)