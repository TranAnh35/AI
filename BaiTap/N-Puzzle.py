import random

class Puzzle():
    def __init__(self, N, start):
        self.N = N
        self.start = start
        self.goal = [[i * N + j + 1 for j in range(N)] for i in range(N)]
        self.goal[-1][-1] = 0
        self.path = {}
        self.visited = set()
        self.q = [start]
        self.visited.add(self.to_string(self.start))
        self.moves = {}
        
    def heuristic(self, state):
        count = 0
        for i in range(self.N):
            for j in range(self.N):
                if state[i][j] != self.goal[i][j]:
                    count += 1
        return count

    def isGoal(self, state):
        return state == self.goal

    def move(self, state):
        next_states = []
        paths = []
        for i in range(self.N):
            for j in range(self.N):
                if state[i][j] == 0:
                    x, y = i, j
                    break
        if x > 0: # up
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[x - 1][y] = new_state[x - 1][y], new_state[x][y]
            next_states.append(new_state)
            paths.append("U")
        if x < self.N - 1: # down
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[x + 1][y] = new_state[x + 1][y], new_state[x][y]
            next_states.append(new_state)
            paths.append("D")
        if y > 0: # left
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[x][y - 1] = new_state[x][y - 1], new_state[x][y]
            next_states.append(new_state)
            paths.append("L")
        if y < self.N - 1: # right
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[x][y + 1] = new_state[x][y + 1], new_state[x][y]
            next_states.append(new_state)
            paths.append("R")
        return next_states, paths

    def printState(self, state):
        for i in range(self.N):
            for j in range(self.N):
                print(state[i][j], end=" ")
            print()
        print()

    def printPath(self, path_list):
        for path in path_list:
            print(path, end=" ")
        print()

    def to_string(self, state):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in state])

    def Breadth_First_Search(self):
        check = True
        while self.q.__len__() > 0:
            state = self.q.pop(0)
            if self.isGoal(state):
                current_state = state
                moves_list = []
                path_list = []
                count_state = 0
                while current_state != self.start:
                    moves_list.append(current_state)
                    path_list.append(self.path[self.to_string(current_state)])
                    count_state += 1
                    current_state = self.moves[self.to_string(current_state)]
                moves_list.append(self.start)
                moves_list.reverse()
                # self.printState(self.start)
                # self.printState(self.goal)
                path_list.reverse()
                for move in moves_list:
                    self.printState(move)
                self.printPath(path_list)
                print("So buoc di: ", count_state)
                check = False
                break
            else:
                next_states, paths = self.move(state)
                for next_state, path in zip(next_states, paths):
                    next_state_str = self.to_string(next_state)
                    if next_state_str not in self.visited:
                        self.q.append(next_state)
                        self.visited.add(next_state_str)
                        self.moves[next_state_str] = state
                        self.path[next_state_str] = path
        if check:
            self.printState(self.start)
            print("Khong tim thay duong di")
        

    def Depth_First_Search(self):
        check = True
        while self.q.__len__() > 0:
            state = self.q.pop()
            if self.isGoal(state):
                current_state = state
                moves_list = []
                path_list = []
                count_state = 0
                while current_state != self.start:
                    moves_list.append(current_state)
                    path_list.append(self.path[self.to_string(current_state)])
                    count_state += 1
                    current_state = self.moves[self.to_string(current_state)]
                moves_list.append(self.start)
                moves_list.reverse()
                # self.printState(self.start)
                # self.printState(self.goal)
                path_list.reverse()
                for move in moves_list:
                    self.printState(move)
                self.printPath(path_list)
                print("So buoc di: ", count_state)
                check = False
                break
            else:
                next_states, paths = self.move(state)
                for next_state, path in zip(next_states, paths):
                    next_state_str = self.to_string(next_state)
                    if next_state_str not in self.visited:
                        self.q.append(next_state)
                        self.visited.add(next_state_str)
                        self.moves[next_state_str] = state
                        self.path[next_state_str] = path
        if check:
            self.printState(self.start)
            print("Khong tim thay duong di")

    def Best_First_Search(self):
        check = True
        
        while self.q.__len__() > 0:
            state = self.q.pop(0)
            
            if self.isGoal(state):
                current_state = state
                moves_list = []
                path_list = []
                count_state = 0
                while current_state != self.start:
                    moves_list.append(current_state)
                    path_list.append(self.path[self.to_string(current_state)])
                    count_state += 1
                    current_state = self.moves[self.to_string(current_state)]
                moves_list.append(self.start)
                moves_list.reverse()
                # self.printState(self.start)
                # self.printState(self.goal)
                path_list.reverse()
                for move in moves_list:
                    self.printState(move)
                self.printPath(path_list)
                print("So buoc di: ", count_state)
                check = False
                break
            else:
                next_states, paths = self.move(state)
                for next_state, path in zip(next_states, paths):
                    next_state_str = self.to_string(next_state)
                    if next_state_str not in self.visited:
                        self.q.append(next_state)
                        self.visited.add(next_state_str)
                        self.moves[next_state_str] = state
                        self.path[next_state_str] = path
                self.q.sort(key=lambda x: self.heuristic(x))
        if check:
            self.printState(self.start)
            print("Khong tim thay duong di")
    
    def Hill_Climbing_Search(self):
        check = True
        
        while self.q.__len__() > 0:
            state = self.q.pop(0)
            if self.isGoal(state):
                current_state = state
                moves_list = []
                path_list = []
                count_state = 0
                while current_state != self.start:
                    moves_list.append(current_state)
                    path_list.append(self.path[self.to_string(current_state)])
                    count_state += 1
                    current_state = self.moves[self.to_string(current_state)]
                moves_list.append(self.start)
                moves_list.reverse()
                # self.printState(self.start)
                # self.printState(self.goal)
                path_list.reverse()
                for move in moves_list:
                    self.printState(move)
                self.printPath(path_list)
                print("So buoc di: ", count_state)
                check = False
                break
            else:
                next_states, paths = self.move(state)
                temp = []
                for next_state, path in zip(next_states, paths):
                    next_state_str = self.to_string(next_state)
                    if next_state_str not in self.visited:
                        temp.append(next_state)
                        self.visited.add(next_state_str)
                        self.moves[next_state_str] = state
                        self.path[next_state_str] = path
                temp.sort(key=lambda x: self.heuristic(x))
                self.q = temp + self.q
        if check:
            self.printState(self.start)
            print("Khong tim thay duong di")

    def Beam_Search(self):
        check = True
        k = 2
        while self.q.__len__() > 0 and check:
            n = min(k, self.q.__len__())
            temp = [self.q.pop(0) for _ in range(n)]
            while temp.__len__() > 0:
                state = temp.pop(0)
                if self.isGoal(state):
                    current_state = state
                    moves_list = []
                    path_list = []
                    count_state = 0
                    while current_state != self.start:
                        moves_list.append(current_state)
                        path_list.append(self.path[self.to_string(current_state)])
                        count_state += 1
                        current_state = self.moves[self.to_string(current_state)]
                    moves_list.append(self.start)
                    moves_list.reverse()
                    # self.printState(self.start)
                    # self.printState(self.goal)
                    path_list.reverse()
                    for move in moves_list:
                        self.printState(move)
                    self.printPath(path_list)
                    print("So buoc di: ", count_state)
                    check = False
                    break
                else:
                    next_states, paths = self.move(state)
                    for next_state, path in zip(next_states, paths):
                        next_state_str = self.to_string(next_state)
                        if next_state_str not in self.visited:
                            self.q.append(next_state)
                            self.visited.add(next_state_str)
                            self.moves[next_state_str] = state
                            self.path[next_state_str] = path
                    self.q.sort(key=lambda x: self.heuristic(x))
        if check:
            self.printState(self.start)
            print("Khong tim thay duong di")    
            
from time import time

if __name__ == "__main__":
    # N = int(input("Nhap N (Nen cho N = 3 thoooi. N lon chay lau lam!!): "))
    # numbers = list(range(N**2))
    # random.shuffle(numbers)
    # start = [numbers[i:i+N] for i in range(0, N**2, N)]
    
    N = 3
    start = [
        [4, 0, 5], 
        [8, 6, 2], 
        [3, 1, 7]]
    
    # N = 3
    # start = [
    #     [0, 7, 4], 
    #     [2, 6, 5], 
    #     [3, 1, 8]]
    
    # start = [
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [0, 7, 8]
    # ]
    
    # N = 4 
    # start = [
    #     [1, 2, 3, 4],
    #     [5, 6, 7, 8],
    #     [9, 10, 0, 11],
    #     [13, 14, 15, 12]
    # ]
    puzzle = Puzzle(N, start)
    chose = int(input("""~~~~~~~ Menu ~~~~~~~
    1. Breadth First Search
    2. Depth First Search
    3. Best First Search
    4. Hill Climbing Search
    5. Beam Search
    0. Exit
    Chose: """))
    if chose == 1:
        time1 = time()
        puzzle.Breadth_First_Search()
        BFS_time = time() - time1
        print('BFS Time:', BFS_time , "\n")
    elif chose == 2:
        puzzle.Depth_First_Search()
    elif chose == 3:
        puzzle.Best_First_Search()
    elif chose == 4:
        puzzle.Hill_Climbing_Search()
    elif chose == 5:
        puzzle.Beam_Search()
    