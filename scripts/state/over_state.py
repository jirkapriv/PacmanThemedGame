

import pygame
from ..state.play_state import Play_State
class Over_State:
    """
    Game state - Over
    """

    def __init__(self, game) -> None:
        self.game = game
        self.font = game.font
        self.text2 = self.font.render(
            "Game Over... Press SPACE to play again", True, (255, 255, 255)
        )

        self.screen = game.screen

    def event_handeler(self) -> None:
        """
        keyboard input hadle
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.game.play_state = Play_State(self.game)
            self.game.current_state = self.game.play_state

    def draw(self) -> None:
        """
        Renders components of game like text
        """
        self.game.screen.fill((0, 0, 0))
        self.screen.blit(self.text2, (10, 50))
