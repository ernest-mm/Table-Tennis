import pygame
from fractions import Fraction

"""
pygame.SCALED can be used to easily scale up the display with a game 
surface blitted on it, but it's hard to scale down all the sprites.
This script will chose what assets' resolution
will be used in the game based on the user's display resolution.
"""
class Display_resolution:
    def __init__(self, development_resolution: tuple[int, int] = (3840, 2160)):
        # Supported display resolutions 
        # (key == tuple of width and height, value == resolution name)
        self.__supported_displays = {
            (3840, 2160): "4k",
            (1920, 1080): "1080p",
            (1280, 720): "720p"
        }

        self.__development_resolution = development_resolution

        self.__user_display_w = None
        self.__user_display_h = None

        # Creating a dictionary that will contain
        # all the information of the game surface.
        self.__game_surf_infos = dict()

    def __assign_display_resolution(self) -> None:
        """
        Assign the user's display width and height to the appropriate attributes.
        Raises a ValueError if the dimensions cannot be retrieved.
        """
        if not pygame.get_init(): # Check if Pygame is already initialized
            pygame.init()

        try:
            display_info = pygame.display.Info()

            # Check for errors

            if display_info.current_w == -1 or display_info.current_h == -1:
                raise ValueError("Unable to retrieve display dimensions.")

            self.__user_display_w, self.__user_display_h = (
                display_info.current_w, 
                display_info.current_h
            )
        
        finally:
            # Only quit pygame if it was initialized by this function
            if pygame.get_init():  # Check if we initialized it here
                pygame.quit()

    def __run_assign_display_resolution(method):
        """
        A decorator that will call __assign_display_resolution 
        before some methods that need it to be called to work.
        """
        def wrapper(self, *args, **kwargs): 
            self.__assign_display_resolution()
            return method(self, *args, **kwargs)
        return wrapper

    def __get_supported_res(self, width: int, height: int) -> tuple[int, int]: 
        """
        Returns either the user's display resolution if it is supported, 
        or a resolution smaller but close enough to it.
        Raises a ValueError if no suitable resolution is found.    
        """

        if (width, height) in self.__supported_displays:
            return (width, height)
        else:

            # Looking for a supported resolution smaller than 
            # the user display but close enough to it

            closest_res = None
            min_diff = float('inf')

            for res in self.__supported_displays.keys():
                res_width, res_height = res
                if width >= res_width and height >= res_height:
                    # Euclidean distance between the resolutions
                    diff = ((res_width - width) ** 2 + (res_height - height) ** 2) ** 0.5

                    if diff < min_diff:
                        min_diff = diff
                        closest_res = res
            
            if closest_res is None:
                raise ValueError(
                    f"Your display resolution ({width} x {height})"
                    " is not supported by the developer."
                )

            return closest_res
        
    def __is_multiple(self) -> bool:
        """
        Checks if the development_resolution is a multiple 
        of all resolutions in the list of supported displays 
        and have the same aspect ratio.
        """
        
        dev_width, dev_height = self.__development_resolution
        
        for (res_width, res_height) in self.__supported_displays.keys():
            # Check if the development resolution 
            # is divisible by the resolution in the 
            # supported_displays dictionary
            if dev_width % res_width != 0 or dev_height % res_height != 0:
                return False
            
            # Check if the aspect ratios match
            width_ratio = dev_width // res_width
            height_ratio = dev_height // res_height
            if width_ratio != height_ratio:
                return False
        
        return True
    
    @__run_assign_display_resolution
    def __get_game_surf_infos(self) -> None:
        """
        Fill self.__game_surf_infos with all the information needed.
        """
        
        # Checking if the developement resolution 
        # is a multiple of every supported display resolution.
        if not self.__is_multiple():
            raise ValueError(
                f"The developer's resolution {self.__development_resolution}" + 
                " should be a multiple of every supported display resolution."
            )
        
        if self.__user_display_w is not None and self.__user_display_h is not None:
            # Getting the best supported resolution for the current display dimensions
            supported_res = self.__get_supported_res(
                self.__user_display_w, 
                self.__user_display_h
            )
        else:
            raise ValueError("Unable to retrieve display dimensions.")

        scale = Fraction(supported_res[0], self.__development_resolution[0])

        self.__game_surf_infos = {
            "size": (supported_res[0], supported_res[1]),
            "width": supported_res[0],
            "height": supported_res[1],
            "resolution": self.__supported_displays[supported_res],
            "scale": scale,
            "user_display_resolution": (self.__user_display_w, self.__user_display_h)
        }

        return None
    
    def __is_value_multiple(self, value: int) -> bool:
        """
        Takes a value and check if that value is a multiple 
        of every supported display resolution's scale factor.
        """
        development_resolution = self.get_development_resolution()
        scale_factors = []

        for res in self.__supported_displays.keys():
            scale = Fraction(res[0], development_resolution[0])
            scale_factors.append(scale)

        for factor in scale_factors:
            value_scaled = value * factor
            if value_scaled.denominator != 1:
                return False
                
        return True

    def __fill_game_surf_infos(self) -> None:
        """
        Calls __get_game_surf_infos to fill self.__game_surf_infos.
        """
        # Check if self.__game_surf_infos has already been filled
        if self.__game_surf_infos:
            return None
        else:
            self.__get_game_surf_infos()

    def __run_fill_game_surf_infos(method):
        """
        A decorator that will call __fill_game_surf_infos 
        before some methods that need it to be called to work.
        """
        def wrapper(self, *args, **kwargs): 
            self.__fill_game_surf_infos()
            return method(self, *args, **kwargs)
        return wrapper
    
    @__run_fill_game_surf_infos
    def scaled_down(self, value: int) -> int:
        """
        Takes a value (x, y, width, or height) in the developer's resolution 
        and returns a value converted to the user's supported resolution.
        """

        scale = self.__game_surf_infos["scale"]

        if scale == 0:
            raise ValueError("Scale factor cannot be zero.")
        
        if not self.__is_value_multiple(value):
            raise ValueError(
                "The value must be a multiple of every" +
                " supported display resolution's scale factor."
            )

        scaled = int(value * scale)

        return scaled

    def get_development_resolution(self) -> tuple[int, int]: 
        """
        Returns the development resolution (width, height).
        """

        dev_res = self.__development_resolution

        return dev_res
    
    @__run_fill_game_surf_infos
    def get_game_surf_size(self) -> tuple[int, int]:
        """
        Returns the user's game surface width and height.
        """

        size = self.__game_surf_infos["size"]

        return size
    
    @__run_fill_game_surf_infos
    def get_game_surf_width(self) -> int:
        """
        Returns the user's game surface width.
        """

        width = self.__game_surf_infos["width"]

        return width
    
    @__run_fill_game_surf_infos
    def get_game_surf_height(self) -> int:
        """
        Returns the user's game surface height.
        """

        height = self.__game_surf_infos["height"]

        return height
    
    @__run_fill_game_surf_infos
    def get_game_surf_res(self) -> str:
        """
        Returns the name of the user's game surface resolution
        """

        res = self.__game_surf_infos["resolution"]

        return res
    
    @__run_fill_game_surf_infos
    def get_game_surf_scale_factor(self) -> Fraction:
        """
        Returns the scale factor of the user's game surface resolution, 
        in relation to the development resolution.
        """

        scale = self.__game_surf_infos["scale"]

        return scale
    
    @__run_fill_game_surf_infos
    def get_user_display_size(self) -> tuple[int, int]:
        """
        Returns the user's display width and height.
        """

        size = self.__game_surf_infos["user_display_resolution"]

        return size
   
if __name__ == "__main__":
    display_res = Display_resolution()
    print(
        f"The screen resolution of this computer is {display_res.get_game_surf_res()}"
    )