import pygame
from scripts.constants import *
from scripts.display_resolution import Display_resolution

def paddle(display_resolution_object: Display_resolution, left_paddle: bool = True) -> dict:
    """
    Returns a dictionary containing the paddle's width, height, x and y coordinates and velocity.
    """
    resolution = display_resolution_object
    width: int = resolution.scaled_down(PADDLE_WIDTH)
    height: int = resolution.scaled_down(PADDLE_HEIGHT)

    if left_paddle:
        x_position: int = resolution.scaled_down(MIN_DISTANCE_FROM_LEFT_OR_RIGHT)
    else:
        x_position: int = resolution.get_screen_width() - resolution.scaled_down(MIN_DISTANCE_FROM_LEFT_OR_RIGHT) - width

    # The paddle height is 1/5 of the screen height, so the y position will be in the middle, at the 3rd position
    y_position: int = height * 2

    velocity = resolution.scaled_down(PADDLE_VELOCITY)

    paddle_infos = {
        "width": width,
        "height": height,
        "x": x_position,
        "y": y_position,
        "velocity": velocity
    }

    return paddle_infos


def draw_paddle(surface: pygame.Surface, color: tuple, paddle: dict) -> None:
    """
    Draw the paddle on a given surface
    """
    paddle["rect"] = pygame.Rect(paddle["x"], paddle["y"], paddle["width"], paddle["height"])
    pygame.draw.rect(surface, color, paddle["rect"])


def ball(display_resolution_object: Display_resolution) -> dict:
    """
    Returns a dictionary containing the ball's center position, x and y coordinates (of the center) and its radius.
    """
    resolution = display_resolution_object
    x_position: int = resolution.get_screen_width() //2
    y_position: int = resolution.get_screen_height() //2
    radius : int = resolution.scaled_down(BALL_RADIUS)

    ball_infos = {
        "x": x_position,
        "y": y_position,
        "center": (x_position, y_position),
        "radius": radius
    }

    return ball_infos


def draw_ball(surface: pygame.Surface, color: tuple, ball: dict) -> None:
    """
    Draw the ball on a given surface
    """
    pygame.draw.circle(surface, color, ball["center"], ball["radius"])
    

if __name__ == "__main__":
    print("This script is only meant to be imported")