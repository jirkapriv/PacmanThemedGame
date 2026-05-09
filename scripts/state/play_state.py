import math
import sys

import pygame

from ..config.config import HEIGHT, INVISIBILITY_TIME
from ..entities.enemies import Enemy
from ..entities.player import Player
from ..map.map import Map


class Play_State:
    """

    Game state - Play
        state of active playing

    Handles important game logic between map, player and enemies

    """

    def __init__(self, game) -> None:
        self.level: int = 1
        self.game = game
        self.map = Map(game)
        self.player = Player(game, self.map)
        self.enemies = [
            Enemy(self, self.map, 440, 200, "cervenak", speed=2),
            Enemy(self, self.map, 440, 200, "ruzovak", speed=2),
            Enemy(self, self.map, 440, 200, "oranzovak", speed=2),
            Enemy(self, self.map, 440, 200, "azurak", speed=2),
        ]
        self.score: int = 0
        self.invisibility = 0
        self.font = game.font
        self.text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.text2 = self.font.render(
            f"Invisibility: {self.invisibility}", True, (255, 255, 255)
        )
        self.text3 = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.text4 = self.font.render(
            "You won!! Now you can Play for best possible score :)",
            True,
            (255, 255, 255),
        )

        self.screen = game.screen
        self.game_won: bool = False
        self.game_over: bool = False
        


    def event_handeler(self) -> None:
        """
        keyboard input hadle
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self) -> None:
        """
        Play state updating, like colisions and game components
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.player.next_action = "left"
        elif keys[pygame.K_RIGHT]:
            self.player.next_action = "right"
        elif keys[pygame.K_UP]:
            self.player.next_action = "up"
        elif keys[pygame.K_DOWN]:
            self.player.next_action = "down"

        self.player.move_player()
        for enemy in self.enemies:
            enemy.update()

        eaten = self.map.check_point_collision(self.player.player_rect)
        if eaten > 0:
            self.score += eaten * 10
            self.text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))

        powered_up = self.map.check_power_up_collision(self.player.player_rect)
        if powered_up > 0:
            self.invisibility = INVISIBILITY_TIME
            self.text2 = self.font.render(
                f"Invisibility: {math.floor(self.invisibility)}", True, (255, 255, 255)
            )
            Enemy.can_kill = False

        if self.map.is_food_empty():
            if self.game.games_lost > 0:
                self.level += 1
            self.text3 = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
            if self.level > 1:
                for x, enemy in enumerate(self.enemies):
                    self.enemies[x].vision_tiles += 1
            if self.level == 4:
                self.game_won = True

        for enemy in self.enemies:
            if Enemy.can_kill and self.player.player_rect.colliderect(
                enemy.player_rect
            ):
                if self.invisibility <= 0:
                    self.game.current_state = self.game.over_state
                    self.game.games_lost +=1

    def draw(self) -> None:
        """
        Renders components of game like text and entities
        """
        if self.invisibility > 0:
            self.invisibility -= 0.1
            self.text2 = self.font.render(
                f"Invisibility: {math.floor(self.invisibility)}", True, (255, 255, 255)
            )
            Enemy.can_kill = False
        else:
            self.invisibility = 0
            self.text2 = self.font.render(
                f"Invisibility: {math.floor(self.invisibility)}", True, (255, 255, 255)
            )
            Enemy.can_kill = True

        self.game.screen.fill((0, 0, 0))
        self.screen.blit(self.text, (10, 10))
        self.screen.blit(self.text2, (10, 50))
        if self.game_won:
            self.screen.blit(self.text4, (10, HEIGHT - 50))
        else:
            self.screen.blit(self.text3, (10, HEIGHT - 50))

        self.map.map_render()
        self.player.render_player()
        for enemy in self.enemies:
            enemy.render()
