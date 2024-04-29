import queue

class WaterJug:
    def __init__(self, jug1, jug2, goal):
        self.jug1 = jug1
        self.jug2 = jug2
        self.goal = goal
        self.visited = set()
        self.q = queue.Queue()
        self.q.put((0, 0))
        self.stack = []
        self.stack.append((0, 0))
        self.visited.add(self.to_string(0, 0))
        self.moves = {}
        
    def isGoal(self, state):
        return state[0] == self.goal or state[1] == self.goal
    
    def to_string(self, x, y):
        return str(x) + " " + str(y)
    
    def move(self, state):
        next_states = []
        paths = []
        if state[0] > 0: # empty jug 1
            new_state = (0, state[1])
            next_states.append(new_state)
            paths.append("E1")
        
        if state[1] > 0: # empty jug 2
            new_state = (state[0], 0)
            next_states.append(new_state)
            paths.append("E2")
            
        if state[0] < self.jug1: # fill jug 1
            new_state = (self.jug1, state[1])
            next_states.append(new_state)
            paths.append("F1")
            
        if state[1] < self.jug2: # fill jug 2
            new_state = (state[0], self.jug2)
            next_states.append(new_state)
            paths.append("F2")
            
        if state[0] > 0 and state[1] < self.jug2: # pour jug 1 to jug 2
            new_state = (max(0, state[0] - (self.jug2 - state[1])), min(self.jug2, state[0] + state[1]))
            next_states.append(new_state)
            paths.append("P12")
            
        if state[1] > 0 and state[0] < self.jug1: # pour jug 2 to jug 1
            new_state = (min(self.jug1, state[0] + state[1]), max(0, state[1] - (self.jug1 - state[0])))
            next_states.append(new_state)
            paths.append("P21")
            
        return next_states, paths
        
    def printState(self, state):
        print(state[0], state[1])
        
    def printPath(self, path_list):
        for path in path_list:
            print(path)
    
    def BFS(self):
        check = True
        while not self.q.empty():
            state = self.q.get()
            if self.isGoal(state):
                check = False
                break
            next_states, paths = self.move(state)
            for i in range(len(next_states)):
                if self.to_string(next_states[i][0], next_states[i][1]) not in self.visited:
                    self.q.put(next_states[i])
                    self.visited.add(self.to_string(next_states[i][0], next_states[i][1]))
                    self.moves[self.to_string(next_states[i][0], next_states[i][1])] = self.to_string(state[0], state[1]) + " " + paths[i]
        
        if check:
            print("No solution")
        else:
            path = []
            goal = state
            while self.to_string(state[0], state[1]) != "0 0":
                path.append(self.moves[self.to_string(state[0], state[1])])
                state = (int(path[-1][0]), int(path[-1][2]))
            path.reverse()
            self.printPath(path)
            self.printState(goal)
            print()
            
    def DFS(self):
        check = True
        while self.stack.__len__() > 0:
            state = self.stack.pop()
            if self.isGoal(state):
                check = False
                break
            next_states, paths = self.move(state)
            for i in range(len(next_states)):
                if self.to_string(next_states[i][0], next_states[i][1]) not in self.visited:
                    self.stack.append(next_states[i])
                    self.visited.add(self.to_string(next_states[i][0], next_states[i][1]))
                    self.moves[self.to_string(next_states[i][0], next_states[i][1])] = self.to_string(state[0], state[1]) + " " + paths[i]
        
        if check:
            print("No solution")
        else:
            path = []
            goal = state
            while self.to_string(state[0], state[1]) != "0 0":
                path.append(self.moves[self.to_string(state[0], state[1])])
                state = (int(path[-1][0]), int(path[-1][2]))
            path.reverse()
            self.printPath(path)
            self.printState(goal)
            print()
            
if __name__ == "__main__":
    jug1, jug2, goal = map(int, input("Nhap the tich binh 1, binh 2 va muc tieu: ").split())
    algo = int(input("Nhap 1 de chon BFS, 2 de chon DFS: "))
    water_jug = WaterJug(jug1, jug2, goal)
    if algo == 1:
        print("BFS:")
        water_jug.BFS()
    elif algo == 2:
        print("DFS:")
        water_jug.DFS()
    else:
        print("Invalid input")