from pathlib import Path
from typing import List

import pygame
import pytmx

from ..config.config import MAP_SCALE, TILE_SIZE

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MAP_PATH = BASE_DIR / "map" / "mapa_pacman.tmx"


class Map:
    """
    Map class
        functions to handle everthing about map
    """

    def __init__(self, game) -> None:
        self.game = game
        self.tmx_map = pytmx.load_pygame(str(MAP_PATH))
        self.point_list: List[pygame.Rect] = []
        self.powerupp_list: List[pygame.Rect] = []

    def can_move(self, rect: pygame.Rect, direction: str) -> bool:
        """
        checks if entity can move in souch direction
        """
        test_rect = rect.copy()

        step = TILE_SIZE

        if direction == "left":
            test_rect.x -= step
        elif direction == "right":
            test_rect.x += step
        elif direction == "up":
            test_rect.y -= step
        elif direction == "down":
            test_rect.y += step

        tile_size = 8 * MAP_SCALE

        tile_x = test_rect.centerx // tile_size
        tile_y = test_rect.centery // tile_size

        return not self.is_wall_tile(tile_x, tile_y)

    def map_render(self):
        """
        renders map and its components
        """
        if self.point_list == []:
            self.get_jidlo()
        if self.powerupp_list == []:
            self.get_poweruppy()

        screen = self.game.screen
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Colides":
                for x, y, image in layer.tiles():
                    image.convert()
                    image.set_colorkey((255, 255, 255))
                    scaled_image = pygame.transform.scale(
                        image, (8 * MAP_SCALE, 8 * MAP_SCALE)
                    )
                    screen.blit(scaled_image, (x * 8 * MAP_SCALE, y * 8 * MAP_SCALE))

        for x, y in enumerate(self.point_list):
            pygame.draw.circle(screen, (255, 255, 255), (y[0], y[1]), 3)

        for x, y in enumerate(self.powerupp_list):
            pygame.draw.circle(screen, (255, 255, 255), (y[0], y[1]), 10)

    def check_point_collision(self, player_rect: pygame.Rect) -> int:
        """
        returns number of points eaten and removes them from point_list
        """
        eaten_list = []
        for point in self.point_list:
            if player_rect.colliderect(point):
                eaten_list.append(point)

        for point in eaten_list:
            self.point_list.remove(point)

        return len(eaten_list)

    def check_power_up_collision(self, player_rect: pygame.Rect) -> int:
        """
        returns number of power ups eaten and removes them from powerupp_list
        """
        eaten_list = []
        for point in self.powerupp_list:
            if player_rect.colliderect(point):
                eaten_list.append(point)

        for point in eaten_list:
            self.powerupp_list.remove(point)

        return len(eaten_list)

    def is_wall_tile(self, tile_x: int, tile_y: int) -> bool:
        """
        checks if a tile is a wall
        """
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Colides":
                try:
                    if layer.data[tile_y][tile_x] != 0:
                        return True
                except IndexError:
                    return False
        return False

    def is_food_empty(self) -> bool:
        """
        function that returns if there is no food on the map
        """
        return len(self.point_list) == 0

    def get_jidlo(self) -> None:
        """
        loads food from pytmx
        """
        if self.point_list == []:
            for layer in self.tmx_map.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Jidlo":
                    for x, y, _ in layer.tiles():
                        self.point_list.append(
                            pygame.Rect(
                                x * 8 * MAP_SCALE + TILE_SIZE // 2 + 4,
                                y * 8 * MAP_SCALE + TILE_SIZE // 2 + 4,
                                2,
                                2,
                            )
                        )

    def get_poweruppy(self) -> None:
        """
        loads power ups from pytmx
        """
        if self.powerupp_list == []:
            for layer in self.tmx_map.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "powerUp":
                    for x, y, _ in layer.tiles():
                        self.powerupp_list.append(
                            pygame.Rect(
                                x * 8 * MAP_SCALE + TILE_SIZE // 2 + 4,
                                y * 8 * MAP_SCALE + TILE_SIZE // 2 + 4,
                                2,
                                2,
                            )
                        )
