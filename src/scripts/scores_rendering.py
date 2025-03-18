import pygame
from scripts.display_resolution import Display_resolution
from scripts.constants import *

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