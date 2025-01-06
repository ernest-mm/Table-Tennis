import pygame
import sys
from scripts.display_resolution import Display_resolution
from scripts.constants import *

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        self.__resolution = Display_resolution()
        self.__screen = pygame.display.set_mode(self.__resolution.get_screen_size(), pygame.SCALED + pygame.FULLSCREEN + pygame.NOFRAME)
        pygame.display.set_caption("Table Tennis")
        self.__clock = pygame.time.Clock()
        # self.ICON = pygame.image.load("PATH")
        # pygame.display.set_icon(self.ICON)

        self.__game_surface = pygame.Surface(self.__resolution.get_screen_size())

    def main_menu(self):
        pass

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.__screen.blit(pygame.transform.scale(self.__game_surface, self.__resolution.get_screen_size()), (0, 0))
            pygame.display.update()
            self.__clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()