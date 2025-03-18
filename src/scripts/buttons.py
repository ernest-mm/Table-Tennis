import pygame
from scripts.scores_rendering import get_text_object
from scripts.constants import *

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
        self.__text = text
        self.__size = size
        self.__surf = surface

        self.__button_bg_infos = None
        self.__button_infos = None

        self.__top_left_x = top_left_x
        self.__top_left_y = top_left_y


    def __get_button_infos(self, size: int = None):
        size = self.__size

        self.__button_bg_infos = get_text_object(
            size, 
            self.__text, 
            BLACK, 
            True, 
            True
        )

        self.__button_infos = get_text_object(
            size,
            self.__text,
            WHITE,
            True,
            False
        )

    def render(self):
        
    