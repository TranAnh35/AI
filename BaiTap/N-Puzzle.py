import queue
import random

class Puzzle():
    def __init__(self, N, start):
        self.N = N
        self.start = start
        self.goal = [[i * N + j + 1 for j in range(N)] for i in range(N)]
        self.goal[-1][-1] = 0
        self.path = {}
        self.visited = set()
        self.q = queue.Queue()
        self.q.put(self.start)
        self.p = []
        self.p.append(self.start)
        self.visited.add(self.to_string(self.start))
        self.moves = {}

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

    def BFS(self):
        check = True
        while not self.q.empty():
            state = self.q.get()
            if self.isGoal(state):
                current_state = state
                moves_list = []
                path_list = []
                while current_state != self.start:
                    moves_list.append(current_state)
                    path_list.append(self.path[self.to_string(current_state)])
                    current_state = self.moves[self.to_string(current_state)]
                moves_list.append(self.start)
                moves_list.reverse()
                path_list.reverse()
                for move in moves_list:
                    self.printState(move)
                self.printPath(path_list)
                check = False
                break
            else:
                next_states, paths = self.move(state)
                for next_state, path in zip(next_states, paths):
                    next_state_str = self.to_string(next_state)
                    if next_state_str not in self.visited:
                        self.q.put(next_state)
                        self.visited.add(next_state_str)
                        self.moves[next_state_str] = state
                        self.path[next_state_str] = path
        if check:
            self.printState(self.start)
            print("Khong tim thay duong di")
        

    def DFS(self):
        check = True
        while self.p.__len__() > 0:
            state = self.p.pop()
            if self.isGoal(state):
                current_state = state
                # moves_list = []
                path_list = []
                while current_state != self.start:
                    # moves_list.append(current_state)
                    path_list.append(self.path[self.to_string(current_state)])
                    current_state = self.moves[self.to_string(current_state)]
                # moves_list.append(self.start)
                # moves_list.reverse()
                self.printState(self.start)
                path_list.reverse()
                self.printState(self.goal)
                # for move in moves_list:
                #     self.printState(move)
                self.printPath(path_list)
                check = False
                break
            else:
                next_states, paths = self.move(state)
                for next_state, path in zip(next_states, paths):
                    next_state_str = self.to_string(next_state)
                    if next_state_str not in self.visited:
                        self.p.append(next_state)
                        self.visited.add(next_state_str)
                        self.moves[next_state_str] = state
                        self.path[next_state_str] = path
        if check:
            self.printState(self.start)
            print("Khong tim thay duong di")    


if __name__ == "__main__":
    N = int(input("Nhap N (Nen cho N = 3 thoooi. N lon chay lau lam!!): "))
    numbers = list(range(N**2))
    random.shuffle(numbers)
    start = [numbers[i:i+N] for i in range(0, N**2, N)]
    # N = 3
    # start = [
    #     [1, 2, 3], 
    #     [4, 5, 6], 
    #     [0, 7, 8]]
    puzzle = Puzzle(N, start)
    # puzzle.BFS()
    puzzle.DFS()
    