import pygame
from fractions import Fraction

# pygame.SCALED can be used to easily scale up the display with a game surface blitted on it, 
# but it's hard to scale down all the sprites.
# This script will chose what assets' resolution will be used in the game based on the user's display resolution.

class Display_resolution:
    def __init__(self, development_resolution: tuple[int, int] = (3840, 2160)):
        # Supported display resolutions (key == tuple of width and height, value == resolution name)
        self.__supported_displays = {
            (3840, 2160): "4k",
            (1920, 1080): "1080p",
            (1280, 720): "720p"
        }

        self.__development_resolution = development_resolution

        # Creating a dictionary that will contain all the information needed for pygame.display.set_mode() with the pygame.SCALED argument.
        self.__screen_infos = dict()

    def __get_dimensions(self) -> tuple[int, int]:
        """
        Returns the user's display width and height.
        Raises a ValueError if the dimensions cannot be retrieved.
        """
        if not pygame.get_init(): # Check if Pygame is already initialized
            pygame.init()

        try:
            display_info = pygame.display.Info()

            # Check for errors

            if display_info.current_w == -1 or display_info.current_h == -1:
                raise ValueError("Unable to retrieve display dimensions.")

            width, height = display_info.current_w, display_info.current_h

            return width, height
        
        finally:
            # Only quit pygame if it was initialized by this function
            if pygame.get_init():  # Check if we initialized it here
                pygame.quit()

    def __get_supported_res(self, width: int, height: int) -> tuple[int, int]: 
        """
        Returns either the user's display resolution if it is supported, or a resolution smaller but close enough to it.
        Raises a ValueError if no suitable resolution is found.    
        """

        if (width, height) in self.__supported_displays:
            return (width, height)
        else:

            # Looking for a supported resolution smaller than the user display but close enough to it

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
                raise ValueError(f"No suitable resolution found for {width}x{height}.")

            return closest_res
        
    def __is_multiple(self) -> bool:
        """
        Checks if the development_resolution is a multiple of all resolutions in the list of supported displays and have the same aspect ratio.
        """
        
        dev_width, dev_height = self.__development_resolution
        
        for (res_width, res_height) in self.__supported_displays.keys():
            # Check if the development resolution is divisible by the resolution in the supported_displays dictionary
            if dev_width % res_width != 0 or dev_height % res_height != 0:
                return False
            
            # Check if the aspect ratios match
            width_ratio = dev_width // res_width
            height_ratio = dev_height // res_height
            if width_ratio != height_ratio:
                return False
        
        return True
    
    def __get_screen_infos(self) -> None:
        """
        Fill self.__screen_infos with all the information needed for pygame.display.set_mode() with the pygame.SCALED argument.
        """
        
        # Checking if the developement resolution is a multiple of every supported display resolution.
        if not self.__is_multiple():
            raise ValueError(f"The developer's resolution {self.__development_resolution} should be a multiple of every supported display resolution.")

        # Getting the display dimensions
        display_width, display_height = self.__get_dimensions()

        # Getting the best supported resolution for the current display dimensions

        supported_res = self.__get_supported_res(display_width, display_height)

        scale = Fraction(supported_res[0], self.__development_resolution[0])

        self.__screen_infos = {
            "size": (supported_res[0], supported_res[1]),
            "width": supported_res[0],
            "height": supported_res[1],
            "resolution": self.__supported_displays[supported_res],
            "scale": scale
        }

        return None
    
    def __is_value_multiple(self, value: int) -> bool:
        """
        Takes a value and check if that value is a multiple of every supported display resolution's scale factor.
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

    def __fill_screen_infos(self) -> None:
        """
        Calls __get_screen_infos to fill self.__screen_infos.
        """
        # Check if self.__screen_infos has already been filled
        if self.__screen_infos:
            return None
        else:
            self.__get_screen_infos()
    
    def scaled_down(self, value: int) -> int:
        """
        Takes a value (x, y, width, or height) in the developer's resolution and returns a value converted to the user's supported resolution.
        """

        scale = self.__screen_infos["scale"]

        if scale == 0:
            raise ValueError("Scale factor cannot be zero.")
        
        if not self.__is_value_multiple(value):
            raise ValueError("The value must be a multiple of every supported display resolution's scale factor.")

        scaled = int(value * scale)

        return scaled

    def get_development_resolution(self) -> tuple[int, int]: 
        """
        Returns the development resolution (width, height).
        """

        dev_res = self.__development_resolution

        return dev_res
    
    def get_screen_size(self) -> tuple[int, int]:
        """
        Returns the user's width and height.
        """

        # Filling self.__screen_infos
        self.__fill_screen_infos()

        size = self.__screen_infos["size"]

        return size

    def get_screen_width(self) -> int:
        """
        Returns the user's screen width.
        """

        # Filling self.__screen_infos
        self.__fill_screen_infos()

        width = self.__screen_infos["width"]

        return width

    def get_screen_height(self) -> int:
        """
        Returns the user's screen height.
        """

        # Filling self.__screen_infos
        self.__fill_screen_infos()

        height = self.__screen_infos["height"]

        return height

    def get_screen_resolution(self) -> str:
        """
        Returns the name of the user's screen resolution
        """

        # Filling self.__screen_infos
        self.__fill_screen_infos()

        res = self.__screen_infos["resolution"]

        return res

    def get_screen_scale_factor(self) -> Fraction:
        """
        Returns the scale factor of the user's screen resolution, in relation to the development resolution.
        """

        # Filling self.__screen_infos
        self.__fill_screen_infos()

        scale = self.__screen_infos["scale"]

        return scale
    
if __name__ == "__main__":
    display_res = Display_resolution()
    print(f"The screen resolution of this computer is {display_res.get_screen_resolution()}")