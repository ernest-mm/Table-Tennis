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
        self.__screen = pygame.display.set_mode(self.__res.get_user_display_size(), pygame.SCALED + pygame.NOFRAME)
        pygame.display.set_caption("Table Tennis")
        # self.ICON = pygame.image.load("PATH")
        # pygame.display.set_icon(self.ICON)
        self.__game_surface = pygame.Surface(self.__res.get_game_surf_size())

        self.__clock = pygame.time.Clock()
        
        # Creating the two paddles
        self.__left_paddle = paddle(self.__res)
        self.__right_paddle = paddle(self.__res, False)

        # Creating the ball
        self.__ball = ball(self.__res)

    def main_menu(self):
        pass

    def __paddle_inside_screen(self, y_coordinate: int, speed: int, up_direction: bool = True) -> bool:
        """
        Returns True if for the next movement, the paddle will be inside the screen. 
        """

        if up_direction:
            if (y_coordinate - speed) > self.__res.scaled_down(MIN_DISTANCE_FROM_TOP):
                return True
        else:
            if y_coordinate + speed < self.__res.scaled_down(MIN_DISTANCE_FROM_BOTTOM):
                return True
            
        return False

    def __paddles_movements(self) -> None:
        """
        Move the paddles up or down depending on which keys have been pressed.
        """

        # Getting the keys that have been pressed
        keys = pygame.key.get_pressed()

        # Setting up the keys for the paddles' up and down movements

        left_paddle_up = pygame.K_w
        left_paddle_down = pygame.K_s

        right_paddle_up = pygame.K_UP
        right_paddle_down = pygame.K_DOWN

        # Moving the paddles only if they are inside the screen

        if keys[left_paddle_up] and self.__paddle_inside_screen(self.__left_paddle["y"], self.__left_paddle["speed"]):
            self.__left_paddle["y"] -= self.__left_paddle["speed"]
        if keys[left_paddle_down] and self.__paddle_inside_screen(self.__left_paddle["y"], self.__left_paddle["speed"], False):
            self.__left_paddle["y"] += self.__left_paddle["speed"]

        if keys[right_paddle_up] and self.__paddle_inside_screen(self.__right_paddle["y"], self.__right_paddle["speed"]):
            self.__right_paddle["y"] -= self.__right_paddle["speed"]
        if keys[right_paddle_down] and self.__paddle_inside_screen(self.__right_paddle["y"], self.__right_paddle["speed"], False):
            self.__right_paddle["y"] += self.__right_paddle["speed"]

    def __ball_movements(self):
        self.__ball["x"] += self.__ball["x_speed"]
        self.__ball["y"] -= self.__ball["y_speed"]

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
            self.__paddles_movements()

            # Here we will handle the ball's movements
            self.__ball_movements()
            
            self.__screen.blit(pygame.transform.scale(self.__game_surface, self.__res.get_game_surf_size()), (0, 0))
            pygame.display.update()
            self.__clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()