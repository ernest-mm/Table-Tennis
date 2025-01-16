import pygame
from scripts.constants import *
from scripts.display_resolution import Display_resolution

def paddle(display_resolution_object: Display_resolution, left_paddle: bool = True) -> dict:
    """
    Returns a dictionary containing the paddle's width, height, x and y coordinates and its rect object.
    """
    resolution = display_resolution_object
    width: int = resolution.scaled_down(PADDLE_WIDTH)
    height: int = resolution.get_screen_height()//5

    if left_paddle:
        x_position: int = resolution.scaled_down(DISTANCE_FROM_HEIGHT)
    else:
        x_position: int = resolution.get_screen_width() - resolution.scaled_down(DISTANCE_FROM_HEIGHT) - width

    # The paddle height is 1/5 of the screen height, so the y position will be in the middle, at the 3rd position
    y_position: int = height * 2

    rect: pygame.Rect = pygame.Rect(x_position, y_position, width, height)

    paddle_infos = {
        "width": width,
        "height": height,
        "x": x_position,
        "y": y_position,
        "rect": rect
    }

    return paddle_infos

def ball(display_resolution_object: Display_resolution) -> dict:
    """
    Returns a dictionary containing the ball's x and y coordinates and its radius.
    """
    resolution = display_resolution_object
    x_position: int = resolution.get_screen_width() //2
    y_position: int = resolution.get_screen_height() //2
    radius : int = resolution.scaled_down(BALL_RADIUS)

    ball_infos = {
        "x": x_position,
        "y": y_position,
        "radius": radius
    }

    return ball_infos