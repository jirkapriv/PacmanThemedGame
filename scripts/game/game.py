import pygame

from ..config.config import HEIGHT, WIDTH
from ..state.play_state import Play_State
from ..state.over_state import Over_State

class Game:
    """
    Main game class

        inits pygame
        handles main loop
        works with game states by ../state/play_state
    """

    def __init__(self) -> None:
        """
        inicialization
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.play_state = Play_State(self)
        self.over_state = Over_State(self)
        self.current_state = self.play_state
        self.games_lost = 0

    def run(self) -> None:
        """
        main game loop
        """
        while self.running:
            self.current_state.event_handeler()
            self.current_state.update()
            self.current_state.draw()
    
            pygame.display.flip()
            self.clock.tick(60)
    
        pygame.quit()
