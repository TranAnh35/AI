from color import Color

class Theme:
    '''
        Stores the game themes data
    '''
    
    def __init__(self, color_bg_light, color_bg_dark, color_trace):
        self.bg_light = Color(color_bg_light)
        self.bg_dark = Color(color_bg_dark)
        self.trace = Color(color_trace)