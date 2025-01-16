import pygame
import sys
from scripts.display_resolution import Display_resolution
from scripts.constants import *
from scripts.entities import paddle, ball

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        if not pygame.get_init():
            raise RuntimeError("Pygame failed to initialize")
        
        # Creating the window and the game surface that will be blitted to the window
        self.__res = Display_resolution()
        self.__screen = pygame.display.set_mode(self.__res.get_screen_size(), pygame.SCALED + pygame.FULLSCREEN + pygame.NOFRAME)
        pygame.display.set_caption("Table Tennis")
        # self.ICON = pygame.image.load("PATH")
        # pygame.display.set_icon(self.ICON)
        self.__game_surface = pygame.Surface(self.__res.get_screen_size())

        self.__clock = pygame.time.Clock()
        
        # Creating the two paddles
        self.__left_paddle = paddle(self.__res)
        self.__right_paddle = paddle(self.__res, False)

        # Creating the ball
        self.__ball = ball(self.__res)

    def main_menu(self):
        pass

    def run(self):
        while True:
            pygame.draw.rect(self.__game_surface, WHITE, self.__left_paddle["rect"])
            pygame.draw.rect(self.__game_surface, WHITE, self.__right_paddle["rect"])
            pygame.draw.circle(self.__game_surface, WHITE, (self.__ball["x"], self.__ball["y"]), self.__ball["radius"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.__screen.blit(pygame.transform.scale(self.__game_surface, self.__res.get_screen_size()), (0, 0))
            pygame.display.update()
            self.__clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()