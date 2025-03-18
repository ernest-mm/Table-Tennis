import pygame
from scripts.display_resolution import Display_resolution
from scripts.constants import *

def draw_table_borders(
        resolution: Display_resolution, 
        surface: pygame.Surface
    ) ->None:
    """
    Adds a white contour to the table
    """
    pygame.draw.line(
        surface,
        SHADOW_WHITE,
        (0, 0),
        (0, resolution.get_game_surf_height()),
        resolution.scaled_down(BALL_RADIUS*2)
    )
    pygame.draw.line(
        surface,
        SHADOW_WHITE,
        (0, resolution.get_game_surf_height()),
        (resolution.get_game_surf_width(), resolution.get_game_surf_height()),
        resolution.scaled_down(BALL_RADIUS*2)
    )
    pygame.draw.line(
        surface,
        SHADOW_WHITE,
        (resolution.get_game_surf_width(), resolution.get_game_surf_height()),
        (resolution.get_game_surf_width(), 0),
        resolution.scaled_down(BALL_RADIUS*2)
    )
    pygame.draw.line(
        surface,
        SHADOW_WHITE,
        (resolution.get_game_surf_width(), 0),
        (0, 0),
        resolution.scaled_down(BALL_RADIUS*2)
    )

def draw_middle_line(
        resolution: Display_resolution, 
        surface: pygame.Surface
    ) -> None:
    """
    Draws an horizontal line in the middle of the table
    """
    start_pos = (
        0,
        resolution.get_game_surf_height() // 2
    )
    end_pos = (
        resolution.get_game_surf_width(),
        resolution.get_game_surf_height() // 2
    )
    pygame.draw.line(
        surface,
        SHADOW_WHITE,
        start_pos,
        end_pos,
        resolution.scaled_down(12)
    )

def draw_net_posts(
        resolution: Display_resolution, 
        surface: pygame.Surface
    ) -> None:
    """
    Draws the net posts of the table
    """
    dev_screen_w, dev_screen_h = resolution.get_development_resolution()

    net_post_w = PADDLE_WIDTH
    net_post_h = BALL_RADIUS * 3

    net_post_x = resolution.scaled_down(dev_screen_w - net_post_w) // 2
    net_post_1_y = 0
    net_post_2_y = resolution.scaled_down(dev_screen_h - net_post_h)

    net_post_1 = pygame.Rect(
        net_post_x,
        net_post_1_y,
        resolution.scaled_down(net_post_w),
        resolution.scaled_down(net_post_h)
    )
    net_post_2 = pygame.Rect(
        net_post_x,
        net_post_2_y,
        resolution.scaled_down(net_post_w),
        resolution.scaled_down(net_post_h)
    )

    # Drawing the net posts
    pygame.draw.rect(surface, BLACK, net_post_1)
    pygame.draw.rect(surface, BLACK, net_post_2)

def draw_net(
        resolution: Display_resolution, 
        surface: pygame.Surface
    ) -> None:
    """
    Draws the net on the table in top view
    """
    net_width = 12
    bottom_net_width = net_width * 2

    dev_screen_w, dev_screen_h = resolution.get_development_resolution()

    start_pos = (
        resolution.scaled_down(dev_screen_w) // 2,
        0
    )
    bottom_net_start_pos = (
        resolution.scaled_down(dev_screen_w) // 2,
        0
    )
    
    end_pos = (
        resolution.scaled_down(dev_screen_w) // 2, 
        resolution.scaled_down(dev_screen_h)
    )
    bottom_net_end_pos = (
        resolution.scaled_down(dev_screen_w) // 2, 
        resolution.scaled_down(dev_screen_h)
    )

    # Drawing the first "line" that will be bellow the second line
    # creating a depth or shadow effect
    pygame.draw.line(
        surface,
        GRAY,
        bottom_net_start_pos,
        bottom_net_end_pos,
        resolution.scaled_down(bottom_net_width)
    )

    # Drawing the top net
    pygame.draw.line(
        surface,
        SHADOW_WHITE,
        start_pos,
        end_pos,
        resolution.scaled_down(net_width)
    )

def render_table(
        resolution: Display_resolution, 
        surface: pygame.Surface
    ) -> None:
    """
    Render the tennis table on the screen
    """
    # Fill the table with green
    surface.fill(FOREST_GREEN)

    draw_middle_line(resolution, surface)

    draw_table_borders(resolution, surface)

    draw_net_posts(resolution, surface)

    draw_net(resolution, surface)