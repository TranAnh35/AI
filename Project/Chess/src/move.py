
class Move:

    def __init__(self, initial, final):
        # initial và final là các đối tượng hình vuông
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final