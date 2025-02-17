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
    net_post_w = (
        resolution.scaled_down(BALL_RADIUS) * 2 - 
        resolution.scaled_down(12)
    )
    net_post_h = resolution.scaled_down(BALL_RADIUS * 3)
    net_post_x = (resolution.get_game_surf_width() - net_post_w) // 2
    net_post_1_y = 0
    net_post_2_y = resolution.get_game_surf_height() - net_post_h

    net_post_1 = pygame.Rect(
        net_post_x,
        net_post_1_y,
        net_post_w,
        net_post_h
    )
    net_post_2 = pygame.Rect(
        net_post_x,
        net_post_2_y,
        net_post_w,
        net_post_h
    )

    # Drawing the net posts
    pygame.draw.rect(surface, BLACK, net_post_1)
    pygame.draw.rect(surface, BLACK, net_post_2)



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
    
    