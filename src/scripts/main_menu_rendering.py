import pygame
from scripts.display_resolution import Display_resolution
from scripts.constants import *

def render_main_menu_bg(
        surface: pygame.Surface,
        resolution: Display_resolution
)-> None:
    """
    Render the main menu background on a surface
    """

    res = resolution.get_game_surf_res()

    bg_img_path = f"{MAIN_MENU_IMG_PATH}{res}_main_menu_background.png"
    bg_img = pygame.image.load(bg_img_path)

    surface.blit(bg_img, (0, 0))

def render_main_menu_title(
        surface: pygame.Surface,
        resolution: Display_resolution
)-> None:
    """
    Render the main menu title on a surface
    """
    res = resolution.get_game_surf_res()

    title_img_path = f"{MAIN_MENU_IMG_PATH}{res}_main_menu_title.png"
    title_img = pygame.image.load(title_img_path)
    title_img_width, title_img_height = title_img.get_size()

    top_left_x = (resolution.get_game_surf_width() - title_img_width) // 2
    top_left_y = title_img_height - title_img_height // 4

    surface.blit(title_img, (top_left_x, top_left_y))