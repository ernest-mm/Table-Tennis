import pygame
import sys
from scripts.display_resolution import Display_resolution
from scripts.constants import *
from scripts.entities import paddle, draw_paddle, ball, draw_ball

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

    def __move_left_paddle(self):
        keys = pygame.key.get_pressed()

        up_key = pygame.K_w
        down_key = pygame.K_s

        # Checking if he's not trying to go outside of the top screen
        if keys[up_key] and self.__left_paddle["y"] > self.__res.scaled_down(MIN_DISTANCE_FROM_TOP):
            self.__left_paddle["y"] -= self.__res.scaled_down(PADDLE_SPEED)

        # Checking if he's not trying to go outside of the bottom screen
        if keys[down_key] and self.__left_paddle["y"] < self.__res.scaled_down(MIN_DISTANCE_FROM_BOTTOM): 
            self.__left_paddle["y"] += self.__res.scaled_down(PADDLE_SPEED)

    def __move_right_paddle(self):
        keys = pygame.key.get_pressed()

        up_key = pygame.K_UP
        down_key = pygame.K_DOWN

        # Checking if he's not trying to go outside of the top screen
        if keys[up_key] and self.__right_paddle["y"] > self.__res.scaled_down(MIN_DISTANCE_FROM_TOP):
            self.__right_paddle["y"] -= self.__res.scaled_down(PADDLE_SPEED)

        # Checking if he's not trying to go outside of the bottom screen
        if keys[down_key] and self.__right_paddle["y"] < self.__res.scaled_down(MIN_DISTANCE_FROM_BOTTOM): 
            self.__right_paddle["y"] += self.__res.scaled_down(PADDLE_SPEED)

    def run(self):

        while True:

            self.__game_surface.fill((0, 0, 0))

            # Drawing the paddles and the ball on the game surface
            draw_paddle(self.__game_surface, WHITE, self.__left_paddle)
            draw_paddle(self.__game_surface, WHITE, self.__right_paddle)
            draw_ball(self.__game_surface, WHITE, self.__ball)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Here we will handle the up and down movements of the paddle. It's outside the event loop because it's a continuous action.
            self.__move_left_paddle()
            self.__move_right_paddle()
            
            self.__screen.blit(pygame.transform.scale(self.__game_surface, self.__res.get_screen_size()), (0, 0))
            pygame.display.update()
            self.__clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()