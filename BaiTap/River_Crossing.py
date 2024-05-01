from audioop import reverse
from copy import deepcopy

class State:
    def __init__(self, left=None, right=None, boat=None):
        self.left = [0, 0, 0, 1, 1, 1] if left is None else left
        self.right = [] if right is None else right
        self.boat = "left" if boat is None else boat
    
    def showStateSimple(self):
        return self.left, "_ " if self.boat == "left" else " _", self.right
    
    def showStatePretty(self):
        pretty_left = ["😇" if x == 0 else "😈" for x in self.left]
        pretty_right = ["😇" if x == 0 else "😈" for x in self.right]
        pretty_boat = " 🚤 ___ " if self.boat == "left" else " ___ 🚤 "
        return ", ".join(pretty_left) + pretty_boat + ", ".join(pretty_right)
    
    def getSides(self):
        return (self.left, self.right) if self.boat == "left" else (self.right, self.left)
    
    def switchBoatSide(self):
        self.boat = "right" if self.boat == "left" else "left"
        
    def move(self, *eles):
        # can only move 1 or 2 people
        if len(eles) - 1 not in range(0, 2):
            return False
        
        _from, to = self.getSides()
        
        if len(eles) == 2:
            if eles[0] == eles[1] and _from.count(eles[0]) < 2:
                # not enough people on shore
                return False
            
            if eles[0] not in _from or eles[1] not in _from:
                # person not on shore
                return False
        else:
            if eles[0] not in _from:
                # person not on shore
                return False
        
        # move people
        for ele in eles:
            _from.remove(ele)
            to.append(ele)
        
        if isGameOver(self):
            return False
        
        self.switchBoatSide()
        self.sort()
        return True
    
    def sort(self):
        self.left = sorted(self.left)
        self.right = sorted(self.right)
        
def isGameOver(s: State):
    # for each shore, check if game is over
    for shore in s.getSides():
        if shore.count(1) > 0 and shore.count(0) > 0:
            if shore.count(1) > shore.count(0):
                # there are more devils than priests on one shore
                return True

    return False

def isWin(s: State):
    if len(s.left) == 0:  # if there is no one on the \
        # starting side of the shore (left), game is won!
        print(
            f"\n\n{s.showStateSimple() if print_method == 'normal' else s.showStatePretty()}"
            + "\n~~~~~~~~ Game Won ~~~~~~~~\n"
        )
        return True
    return False

def rollBack(s, eles) -> State:
    startState = deepcopy(s)
    
    if not s.move(*eles):
        print("\nThat move ends the game!")
        return startState
    return s

print_method = "emoji"

def manualPlay(s: State):
    global print_method
    
    if isGameOver(s):
        return False
    
    if isWin(s):
        return True
    
    if print_method == "emoji":
        print("\n" + s.showStatePretty())
    else:
        print("\n" + str(s.showStateSimple()))
        
    choice = input(printManualPlayMenu())
    
    if choice == "1":
        manualPlay(rollBack(s, [0]))
    
    if choice == "2":
        manualPlay(rollBack(s, [0, 0]))
        
    if choice == "3":
        manualPlay(rollBack(s, [1]))
        
    if choice == "4":
        manualPlay(rollBack(s, [1, 1]))
    
    if choice == "5":
        manualPlay(rollBack(s, [0, 1]))
        
    if choice.upper() == "R":
        print(printNewGame())
        manualPlay(State())
        
    if choice.upper() == "P":
        print_method = "emoji" if print_method == "normal" else "normal"
        manualPlay(s)
        
    if choice == "0":
        return False
    
possible_moves = [[0], [0, 0], [1], [1, 1], [0, 1]]
visited, q = [], []
moves = {}
count_states = 0    

def solve(s: State, mode='dfs', verbose=False):
    global count_states
    
    if isWin(s):
        printState(s, verbose)
        print(f"{mode.upper()} solved in {count_states} moves")
        return True
    
    count_states += 1
    
    for move in possible_moves:
        temp_state = deepcopy(s)
        
        if temp_state.move(*move):
            t = (str(temp_state.showStateSimple()), move)
            if t not in visited:
                visited.append(t)
                q.append(temp_state)
                if str(temp_state.showStateSimple()) not in moves:
                    moves[str(temp_state.showStateSimple())] = {
                        'prev_states': [s],
                        'move': [move]}
                else:
                    moves[str(temp_state.showStateSimple())]['prev_states'].append(s)
                    moves[str(temp_state.showStateSimple())]['move'].append(move)
    
    solve(q.pop((len(q) - 1) if mode == "dfs" else 0), mode, verbose)
    
def reverseSide(side):
    return "phai" if side == "left" else "trai"
    
def printPath(state, path, mode):
    if mode:
        pretty_path = ["😇" if x == 0 else "😈" for x in path]
        print( "Chuyen " + ", ".join(pretty_path) + " sang bo " + reverseSide(state.boat))
    else:
        simple_path = ["0" if x == 0 else "1" for x in path]
        print( "Chuyen " + ", ".join(simple_path) + " sang bo " + reverseSide(state.boat))
    
    
def printState(s: State, mode):
    current_state = s
    start_state = State()
    moves_list = []
    path_list = []
    while str(current_state.showStateSimple()) != str(start_state.showStateSimple()):
        moves_list.append(current_state)
        path_list.append(moves[str(current_state.showStateSimple())]['move'][0])
        current_state = moves[str(current_state.showStateSimple())]['prev_states'][0]
    moves_list.append(start_state)
    moves_list.reverse()
    # path_list.reverse()
    for state in moves_list:
        print(state.showStatePretty() if mode else state.showStateSimple())
        print()
        if path_list:
            printPath(state, path_list.pop(), mode)

def printMenu():
    return """
    1. Choi game
    2. Giai bang DFS
    2v. Giai bang DFS (vip)
    3. Giai bang BFS
    3v. Giai bang BFS (vip)
    0. Thoat
    """
    
def printManualPlayMenu():
    return """
    1. Di chuyen 1 thay tu 😇
    2. Di chuyen 2 thay tu 😇😇
    3. Di chuyen 1 con quy 😈
    4. Di chuyen 2 con quy 😈😈
    5. Di chuyen 1 thay tu and 1 con quy 😇😈
    R. Restart game
    P. Chuyen phuong thuc in (sang kieu so)
    0. Thoat

    """ * (
        print_method == "emoji"
    ) + """
    1. Di chuyen 1 thay tu [0]
    2. Di chuyen 2 thay tu [0 0]
    3. Di chuyen 1 con quy [1]
    4. Di chuyen 1 con quy [1 1]
    5. Di chuyen 1 thay tu and 1 con quy [0 1]
    R. Restart game
    P. Chuyen phuong thuc in (sang kieu emoji)
    0. Thoat

    """ * (
        print_method == "normal"
    )

def printNewGame():
    return "\n~~~~~~~~ New Game ~~~~~~~~"

if __name__ == "__main__":
    while (menu := input(printMenu())) != "0":
        
        visited, q = [], []
        count_states = 0
        
        print(menu)
        
        if menu == "1":
            while manual := manualPlay(State()):
                print(printNewGame())
            
        if menu == "2":
            solve(State())
            
        if menu == "2v":
            solve(State(), verbose=True)
            
        if menu == "3":
            solve(State(), mode="bfs")
            
        if menu == "3v":
            solve(State(), mode="bfs", verbose=True)
            
        if menu == "0":
            break
    
    print("Bye bye! 👋")