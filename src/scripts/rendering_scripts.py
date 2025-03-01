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

def get_text_object(
        font_size: int, 
        text: str, 
        text_color: tuple, 
        anti_aliasing: bool,
        is_bold: bool
    ) -> dict:

    pygame.font.init()
    font = pygame.font.Font(FONT_PATH, font_size)

    if is_bold:
        base_text = font.render(text, anti_aliasing, text_color)
        text_surface = pygame.Surface(
            base_text.get_size(), 
            pygame.SRCALPHA
        )

        offsets = [(0, 0), (1, 0), (0, 1), 
                   (1, 1), (2, 0), (0, 2), 
                   (2, 1), (1, 2), (-1, 0), 
                   (0, -1), (-1, -1), (-1, 1), 
                   (1, -1)
        ]

        for dx, dy in offsets:
            text_surface.blit(
                font.render(text, anti_aliasing, text_color), 
                (dx, dy)
            )

        text_w, text_h = text_surface.get_size()

    else:
        text_surface = font.render(text, anti_aliasing, text_color)
        text_w, text_h = text_surface.get_size()

    return_value = {
        "text": text_surface,
        "width": text_w,
        "height": text_h
    }
    return return_value

def render_scores_text(
        text: str,
        left_score: int,
        right_score: int,
        surface: pygame.Surface,
        resolution: Display_resolution,
        is_match_score: bool = True
    ) -> None:
    """
    Render the match won or score texts on the game surface
    """
    font_size = resolution.scaled_down(SCORES_FONT_SIZE)

    text_infos = get_text_object(
        font_size,
        text,
        WHITE,
        True,
        False
    )

    score_infos = get_text_object(
        font_size,
        f"{left_score} - {right_score}",
        WHITE,
        True,
        False
    )

    text_shadow_infos = get_text_object(
        font_size,
        text,
        BLACK,
        True,
        True
    )

    score_shadow_infos = get_text_object(
        font_size,
        f"{left_score} - {right_score}",
        BLACK,
        True,
        True
    )

    text_x = (resolution.get_game_surf_width() - text_infos["width"]) // 2
    score_x = (resolution.get_game_surf_width() - score_infos["width"]) // 2
    text_shadow_x = (resolution.get_game_surf_width() - text_shadow_infos["width"]) // 2
    score_shadow_x = (resolution.get_game_surf_width() - score_shadow_infos["width"]) // 2
    
    if is_match_score:
        text_y = resolution.scaled_down(MATCH_TEXT_Y)
        score_y = resolution.scaled_down(MATCH_TEXT_Y) + score_infos["height"]
        text_shadow_y = resolution.scaled_down(MATCH_TEXT_Y)
        score_shadow_y = resolution.scaled_down(MATCH_TEXT_Y) + score_infos["height"]
    else:
        y = MATCH_TEXT_Y + (score_infos["height"] * 4)
        text_y = resolution.scaled_down(y)
        score_y = resolution.scaled_down(y) + score_infos["height"]
        text_shadow_y = resolution.scaled_down(y)
        score_shadow_y = resolution.scaled_down(y) + score_infos["height"]

    surface.blit(
        text_shadow_infos["text"],
        (text_shadow_x, text_shadow_y)
    )

    surface.blit(
        text_infos["text"],
        (text_x, text_y)
    )

    surface.blit(
        score_shadow_infos["text"],
        (score_shadow_x, score_shadow_y)
    )

    surface.blit(
        score_infos["text"],
        (score_x, score_y)
    )

def render_match_won(
        left_score: int,
        right_score: int,
        surface: pygame.Surface,
        resolution: Display_resolution,
    ) -> None:
    """
    Render the match won on the game surface
    """
    render_scores_text(
        "MATCH WON",
        left_score,
        right_score,
        surface,
        resolution
    )

def render_scores(
        left_score: int,
        right_score: int,
        surface: pygame.Surface,
        resolution: Display_resolution,
    ) -> None:
    """
    Render the scores of a match on the game surface
    """
    render_scores_text(
        f"SCORES",
        left_score,
        right_score,
        surface,
        resolution,
        False
    )

def render_text(
        text: str,
        text_color: tuple,
        font_size: int,
        top_left: tuple,
        surface: pygame.Surface,
        anti_aliasing: bool,
        resolution: Display_resolution, 
        is_bold: bool = False
    ) -> pygame.Surface:

    text_infos = get_text_object(
        font_size,
        text,
        text_color,
        anti_aliasing,
        is_bold
    )

    surface.blit(text_infos["text"], top_left)

    return surface

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