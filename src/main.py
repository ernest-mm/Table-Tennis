import pygame
import sys
from scripts.display_resolution import Display_resolution
from scripts.constants import *
from scripts.entities import paddle, draw_paddle, ball, draw_ball
from scripts.table_rendering import render_table
from scripts.main_menu_rendering import render_main_menu_bg, render_main_menu_title
from scripts.scores_rendering import render_match_won, render_scores
from scripts.buttons import Button

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        if not pygame.get_init():
            raise RuntimeError("Pygame failed to initialize")
        
        # Creating the window and the game surface that will be blitted to the window
        self.__res = Display_resolution()
        self.__screen = pygame.display.set_mode(
            self.__res.get_game_surf_size(),
            pygame.SCALED | pygame.FULLSCREEN | pygame.NOFRAME
        )
        pygame.display.set_caption("Table Tennis")
        # self.ICON = pygame.image.load("PATH")
        # pygame.display.set_icon(self.ICON)
        self.__game_surface = pygame.Surface(self.__res.get_game_surf_size())

        self.__clock = pygame.time.Clock()
        
        # Creating the two paddles
        self.__left_paddle = paddle(self.__res)
        self.__right_paddle = paddle(self.__res, False)

        # Creating the ball and a variable that will contain the
        # in game ball's x speed
        self.__ball = ball(self.__res, self.__res.scaled_down(BALL_X_SPEED))
        self.__ball_x_speed = self.__res.scaled_down(BALL_X_SPEED)

        # A variable that will store the boolean
        # telling if there is a match playing or not
        self.__playing = False

        # Match won and scores
        self.__left_scores = {
            "match_won": 0,
            "score": 0
        }
        self.__right_scores = {
            "match_won": 0,
            "score": 0
        }

    def __start_match(self) -> None:
        """
        Start the match if it hasn't started by making the ball move
        """
        # Getting the keys that have been pressed
        keys = pygame.key.get_pressed()

        left_paddle_up = self.__left_paddle["up_key"]
        left_paddle_down = self.__left_paddle["down_key"]

        right_paddle_up = self.__right_paddle["up_key"]
        right_paddle_down = self.__right_paddle["down_key"]

        if self.__playing == False:
            if keys[left_paddle_up] or keys[left_paddle_down]:
                self.__ball["x_speed"] *= -1
                self.__playing = True
            elif keys[right_paddle_up] or keys[right_paddle_down]:
                self.__playing = True
    
    def __paddle_inside_screen(
            self, 
            y_coordinate: int, 
            speed: int, 
            up_direction: bool = True
        ) -> bool:
        """
        Returns True if for the next movement, the paddle will be inside the screen. 
        """

        if up_direction:
            if (y_coordinate - speed) > self.__res.scaled_down(MIN_DISTANCE_FROM_TOP):
                return True
        else:
            if (y_coordinate + speed) < self.__res.scaled_down(MIN_DISTANCE_FROM_BOTTOM):
                return True
            
        return False

    def __paddles_movements(self) -> None:
        """
        Move the paddles up or down depending on which keys have been pressed.
        """

        # Getting the keys that have been pressed
        keys = pygame.key.get_pressed()

        left_paddle_up = self.__left_paddle["up_key"]
        left_paddle_down = self.__left_paddle["down_key"]

        right_paddle_up = self.__right_paddle["up_key"]
        right_paddle_down = self.__right_paddle["down_key"]

        # Moving the paddles only if they are inside the screen

        if (keys[left_paddle_up] and 
                self.__paddle_inside_screen(
                    self.__left_paddle["y"], 
                    self.__left_paddle["speed"]
                )):
            self.__left_paddle["y"] -= self.__left_paddle["speed"]

        if (keys[left_paddle_down] and 
                self.__paddle_inside_screen(
                    self.__left_paddle["y"], 
                    self.__left_paddle["speed"], 
                    False
                )):
            self.__left_paddle["y"] += self.__left_paddle["speed"]

        if (keys[right_paddle_up] and 
                self.__paddle_inside_screen(
                    self.__right_paddle["y"], 
                    self.__right_paddle["speed"]
                )):
            self.__right_paddle["y"] -= self.__right_paddle["speed"]

        if (keys[right_paddle_down] and 
                self.__paddle_inside_screen(
                    self.__right_paddle["y"], 
                    self.__right_paddle["speed"], 
                    False
                )):
            self.__right_paddle["y"] += self.__right_paddle["speed"]

    def __top_bottom_collisions(self) -> None:
        """
        Handles the collisions of the ball with the top and bottom 
        of the screen
        """
        if (self.__ball["y"] + self.__ball["radius"] >= 
            self.__res.get_game_surf_height()):
            self.__ball["y_speed"] *= -1

        elif self.__ball["y"] - self.__ball["radius"] <= 0:
            self.__ball["y_speed"] *= -1

    def __ball_angle_change(self, left_paddle: bool = True) -> None:
        """
        Changes the angle of the ball based on where it hits 
        the paddle
        """
        if left_paddle:
            paddle = self.__left_paddle
        else:
            paddle = self.__right_paddle

        middle_y = paddle["y"] + (paddle["height"] // 2)
        difference_in_y = middle_y - self.__ball["y"]
        reduction_factor = (paddle["height"] / 2) / self.__ball["x_speed"]
        y_speed = difference_in_y / reduction_factor
        self.__ball["y_speed"] = -1 * y_speed

    def __collisions(self) -> None:
        """
        Handles all the collisions of the ball
        """
        # Collision with the top and bottom of the screen
        self.__top_bottom_collisions()

        # Collision with the left paddle
        if self.__ball["x_speed"] < 0:
            if (self.__ball["y"] >= self.__left_paddle["y"] and 
                    self.__ball["y"] <= self.__left_paddle["y"] + self.__left_paddle["height"]):
                if (self.__ball["x"] - self.__ball["radius"] <= 
                        self.__left_paddle["x"] + self.__left_paddle["width"]):
                    self.__ball["x_speed"] *= -1
                    self.__ball_angle_change()

        else:
            # Collision with the right paddle
            if (self.__ball["y"] >= self.__right_paddle["y"] and 
                    self.__ball["y"] <= self.__right_paddle["y"] + self.__right_paddle["height"]):
                if (self.__ball["x"] + self.__ball["radius"] >= 
                        self.__right_paddle["x"]):
                    self.__ball["x_speed"] *= -1
                    self.__ball_angle_change(False)

    def __ball_movements(self) -> None:
        if self.__playing:
            self.__ball["x"] += self.__ball["x_speed"]
            self.__ball["y"] -= self.__ball["y_speed"]

    def __new_match(self) -> None:
        """
        Reset the positions of the paddles and ball to start a new match
        """
        self.__left_paddle = paddle(self.__res)
        self.__right_paddle = paddle(self.__res, False)
        self.__ball = ball(self.__res, self.__ball_x_speed)
        # Ensure the ball's speed matches the current base speed
        self.__ball["x_speed"] = self.__ball_x_speed
        self.__playing = False

    def __check_winner(self) -> None:
        """
        Checks whether the ball has gone of the left or right screen
        and updates the paddle's score, match_won and ball_x_speed accordingly
        """
        if self.__ball["x"] + self.__ball["radius"] < 0:
            self.__right_scores["score"] += 1
            # Make the ball faster by increasing the absolute value of the speed
            # Use a percentage-based increase that gets smaller as the score gets higher
            speed_increase = self.__res.scaled_down(BALL_X_SPEED_VARIATION) * (1 / (1 + self.__right_scores["score"] * 0.1))
            if self.__ball["x_speed"] < 0:
                self.__ball_x_speed -= speed_increase
            else:
                self.__ball_x_speed += speed_increase
            if self.__right_scores["score"] >= 10:
                self.__left_scores["score"] = 0
                self.__right_scores["score"] = 0
                self.__right_scores["match_won"] += 1
                self.__ball_x_speed = self.__res.scaled_down(BALL_X_SPEED)
                self.__new_match()
            else:
                self.__new_match()

        elif (self.__ball["x"] - self.__ball["radius"] >
                self.__res.get_game_surf_width()):
            self.__left_scores["score"] += 1
            # Make the ball faster by increasing the absolute value of the speed
            # Use a percentage-based increase that gets smaller as the score gets higher
            speed_increase = self.__res.scaled_down(BALL_X_SPEED_VARIATION) * (1 / (1 + self.__left_scores["score"] * 0.1))
            if self.__ball["x_speed"] < 0:
                self.__ball_x_speed -= speed_increase
            else:
                self.__ball_x_speed += speed_increase
            if self.__left_scores["score"] >= 10:
                self.__left_scores["score"] = 0
                self.__right_scores["score"] = 0
                self.__left_scores["match_won"] += 1
                self.__ball_x_speed = self.__res.scaled_down(BALL_X_SPEED)
                self.__new_match()
            else:
                self.__new_match()

    def main_menu(self):
        new_game_button = Button(
            self.__game_surface,
            "NEW GAME",
            self.__res.scaled_down(102),
            0,
            0
        )
        quit_button = Button(
            self.__game_surface,
            "QUIT",
            self.__res.scaled_down(102),
            0,
            0
        )

        new_game_button_top_x = (self.__res.get_game_surf_width() - new_game_button.get_width()) // 2
        new_game_button_top_y = self.__res.scaled_down(1200)

        quit_button_top_x = (self.__res.get_game_surf_width() - quit_button.get_width()) // 2
        quit_button_top_y = new_game_button_top_y + self.__res.scaled_down(210)

        new_game_button = Button(
            self.__game_surface,
            "NEW GAME",
            self.__res.scaled_down(102),
            new_game_button_top_x,
            new_game_button_top_y
        )
        quit_button = Button(
            self.__game_surface,
            "QUIT",
            self.__res.scaled_down(102),
            quit_button_top_x,
            quit_button_top_y
        )

        while True:
            render_main_menu_bg(self.__game_surface, self.__res)
            render_main_menu_title(self.__game_surface, self.__res)

            mouse_position = pygame.mouse.get_pos()

            new_game_button.render(mouse_position)
            quit_button.render(mouse_position)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if new_game_button.mouse_hover(mouse_position):
                        return self.run()
                    if quit_button.mouse_hover(mouse_position):
                        pygame.quit()
                        sys.exit()

            self.__screen.blit(
                pygame.transform.scale(self.__game_surface, self.__res.get_game_surf_size()), 
                (0, 0)
            )
            pygame.display.update()
            self.__clock.tick(FPS)


    def run(self):

        while True:
            render_table(self.__res, self.__game_surface)

            # Drawing the paddles and the ball on the game surface
            draw_paddle(self.__game_surface, self.__left_paddle)
            draw_paddle(self.__game_surface, self.__right_paddle)
            draw_ball(self.__game_surface, WHITE, self.__ball)

            render_match_won(
                self.__left_scores["match_won"],
                self.__right_scores["match_won"],
                self.__game_surface,
                self.__res
            )

            render_scores(
                self.__left_scores["score"],
                self.__right_scores["score"],
                self.__game_surface,
                self.__res
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.__start_match()

            # Here we will handle the up and down movements of the paddle. 
            # It's outside the event loop because it's a continuous action.
            self.__paddles_movements()

            # Here we will handle the ball's movements
            self.__ball_movements()

            # Handleling the collisions
            self.__collisions()

            self.__check_winner()

            self.__screen.blit(
                pygame.transform.scale(self.__game_surface, self.__res.get_game_surf_size()), 
                (0, 0)
            )
            pygame.display.update()
            self.__clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.main_menu()