import pygame
from scripts.scores_rendering import get_text_object
from scripts.constants import *
from scripts.display_resolution import Display_resolution

class Button:
    def __init__(
        self,
        surface: pygame.Surface,
        text: str,
        size: int,
        top_left_x: int,
        top_left_y: int    
    ):
        self.__size = size
        self.__button_text = text
        self.__surf = surface

        self.__button_bg_infos = None
        self.__button_infos = None
        self.__button_rect = None

        self.__button_x = top_left_x
        self.__button_y = top_left_y


    def __get_button_infos(self) -> None:
        """
        Fills self.__button_bg_infos, self.__button_infos and
        self.__button_rect
        """

        size = self.__size

        self.__button_bg_infos = get_text_object(
            size, 
            self.__button_text, 
            BLACK, 
            True, 
            True
        )

        self.__button_infos = get_text_object(
            size,
            self.__button_text,
            WHITE,
            True,
            False
        )

        self.__button_rect = pygame.Rect(
            self.__button_x,
            self.__button_y,
            self.__button_bg_infos["width"],
            self.__button_bg_infos["height"]
        )

    def mouse_hover(self, mouse_pos: tuple) -> bool:
        """
        Returns True if the mouse is hovering the button
        """
        if self.__button_rect.collidepoint(mouse_pos):
            return True
        
        return False


    def render(self, mouse_pos: tuple) -> None:
        """
        Render the button on the screen
        """

        self.__get_button_infos()

        if self.mouse_hover(mouse_pos):
            true_size = self.__size
            self.__size = int(self.__size * 1.5)
            self.__get_button_infos()
            self.__size = true_size 

        self.__surf.blit(
            self.__button_bg_infos["text"],
            (self.__button_x, self.__button_y)
        )

        self.__surf.blit(
            self.__button_infos["text"],
            (self.__button_x, self.__button_y)
        )

    def get_width(self) -> int:
        "Returns the width of the button"
        self.__get_button_infos()

        return self.__button_bg_infos["width"]
    
    def get_height(self) -> int:
        "Returns the height of the button"
        self.__get_button_infos()

        return self.__button_bg_infos["height"]