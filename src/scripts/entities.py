import pygame
from scripts.constants import *
from scripts.display_resolution import Display_resolution

class Paddle():
    # def __init__(self, left: int, top: int, width: int, height: int, screen_width: int, screen_height: int, left_paddle: bool = True):
    #     # Call the parent constructor to initialize the rectangle
    #     super().__init__(left, top, width, height)

    #     self.__res = Display_resolution()
        
    #     self.__width: int = self.__res.scaled_down(PADDLE_WIDTH)
    #     self.__height: int = self.__res.get_screen_height()//5

    #     if left_paddle:
    #         self.__x_position: int = self.__res.scaled_down(DISTANCE_FROM_HEIGHT)
    #     else:
    #         self.__x_position: int = self.__res.get_screen_width() - self.__res.scaled_down(DISTANCE_FROM_HEIGHT) - self.__width
        
    #     # The paddle height is 1/5 of the screen height, so the y position will be in the middle, at the 3rd position
    #     self.__y_position: int = self.__height * 2

    # def x(self, x: int =):

    def __init__(self, left_paddle: bool = True):
        if not pygame.get_init(): # Check if Pygame is already initialized
            pygame.init()
            
        self.__res = Display_resolution()
        self.__width: int = self.__res.scaled_down(PADDLE_WIDTH)
        self.__height: int = self.__res.get_screen_height()//5

        if left_paddle:
            self.__x_position: int = self.__res.scaled_down(DISTANCE_FROM_HEIGHT)
        else:
            self.__x_position: int = self.__res.get_screen_width() - self.__res.scaled_down(DISTANCE_FROM_HEIGHT) - self.__width
        
        # The paddle height is 1/5 of the screen height, so the y position will be in the middle, at the 3rd position
        self.__y_position: int = self.__height * 2
        
        self.__rect: pygame.Rect = pygame.Rect(self.__x_position, self.__y_position, self.__width, self.__height)

    def y(self, y: int) -> None:
        """
        Set the new y postion of the paddle
        """
        self.__y_position = y

    def get_x(self) -> int:
        """
        Returns the x position of the paddle
        """
        x = self.__x_position
        
        return x

    def get_y(self) -> int:
        """
        Returns the y position of the paddle
        """
        y = self.__y_position

        return y
    
    def get_width(self) -> int:
        """
        Returns the width of the paddle
        """
        width = self.__width
        
        return width
    
    def get_height(self) -> int:
        """
        Returns the height of the paddle
        """
        height = self.__height
        
        return height
    
    def get_rect(self) -> pygame.Rect:
        """
        Returns the rect object of the paddle
        """
        rect = self.__rect

        return rect
   

class Ball:
    def __init__(self, surface: pygame.Surface, screen_width: int, screen_height: int):
        self.__surface = surface
        self.__resolution = Display_resolution()
        self.__x_position: int = screen_width//2
        self.__y_position: int = screen_height//2
        self.__radius : int = self.__resolution.scaled_down(BALL_RADIUS)
    
    def draw(self):
        pygame.draw.circle(self.__surface, WHITE, (self.__x_position, self.__y_position), self.__radius)
