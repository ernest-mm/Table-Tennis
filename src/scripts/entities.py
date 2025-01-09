import pygame

class Paddle:
    pass

class Ball:
    def __init__(self, surface: pygame.Surface, screen_width: int, screen_height: int):
        self.surface = surface
        self.x_position: int = screen_width//2
        self.y_position: int = screen_height//2
        pass
    
    def draw(self):
        pygame.draw.circle(self.surface, (255, 255, 255), (self.x_position, self.y_position), 40)
