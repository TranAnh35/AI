import os, pygame

class Piece:
    '''
        Creates the game pieces
    '''
    
    def __init__(self, name):
        self.name = name
        self.set_texture()
        
    def __str__(self):
        return self.name.upper()
    
    # -------------
    # Class methods
    # -------------
        
    def set_texture(self):
        self.texture = os.path.join(f'assets/images/{self.name}.png')
        
                    
class X(Piece):
    def __init__(self):
        super().__init__('x')
        
class O(Piece):
    def __init__(self):
        super().__init__('o')