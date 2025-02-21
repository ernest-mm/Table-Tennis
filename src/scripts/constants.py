# Game's frame per second
FPS: int = 60

# Ball's diameter size in 4k 
BALL_RADIUS: int = 36

# Paddle's width in 4K
PADDLE_WIDTH: int = BALL_RADIUS * 2
PADDLE_HEIGHT: int = 2160 // 5

PADDLE_SPEED: int = 18

# Minimum distance of the paddle from the left 
# or right of the screen in 4k
MIN_DISTANCE_FROM_LEFT_OR_RIGHT: int = BALL_RADIUS//2
# Minimum distance of the paddle from the top of the screen in 4k
MIN_DISTANCE_FROM_TOP: int = MIN_DISTANCE_FROM_LEFT_OR_RIGHT
# Minimum distance of the paddle from the bottom of the screen in 4k
MIN_DISTANCE_FROM_BOTTOM: int = (
    2160 - PADDLE_HEIGHT - MIN_DISTANCE_FROM_LEFT_OR_RIGHT
)

# Colors
WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)
SHADOW_WHITE: tuple = (210, 210, 210)
GRAY: tuple = (128, 128, 128)
FOREST_GREEN: tuple = (0, 102, 0)

# PATHS
PADDLES_IMG_PATH: str = "assets/images/paddles/"
FONT_PATH: str = "assets/fonts/Boogaloo-Regular.ttf"

# "Match won" and "Scores" font size in 4k
SCORES_FONT_SIZE: int = 54

# "Match won" text y position in 4k
MATCH_TEXT_Y: int = 120

BALL_X_SPEED: int = -24
BALL_X_SPEED_VARIATION:int = 6