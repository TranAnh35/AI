class State:
    greedy_evaluation = None
    AStar_evaluation = None
    heuristic = None
    
    def __init__(self, state, parent, diretion, depth, cost):
        self.state = state
        self.parent = parent
        self.direction = diretion
        self.depth = depth
        self.cost = cost
        self.goal = [i for i in range(1, len(state))] + [0]
        
        if parent:
            self.cost = parent.cost + cost
        else:
            self.cost = cost
            
    def isGoal(self): # kiểm tra xem state hiện tại có phải là goal không
        if self.state == self.goal:
            return True
        return False
    
    def Manhattan_Distance(self, n): # Hàm Heuristic dựa trên khoảng cách Manhattan
        self.heuristic = 0
        
        for i in range(1, n*n):
            distance = abs(self.state.index(i) - self.goal.index(i))
            
            # khoảng cách Manhattan giữa trạng thái hiện tại và trạng thái mục tiêu
            self.heuristic += distance / n + distance % n
        
        self.greedy_evaluation = self.heuristic
        self.AStar_evaluation = self.heuristic + self.cost
        
        return ( self.greedy_evaluation, self.AStar_evaluation)
    
    # hàm heuristic dựa trên số lượng ô đặt sai vị trí
    def Misplaced_Tiles(self,n): 
        counter = 0;
        self.heuristic = 0
        for i in range(n*n):
            for j in range(n*n):
                if (self.state[i] != self.goal[j]):
                    counter += 1
                self.heuristic = self.heuristic + counter

        self.greedy_evaluation = self.heuristic    
        self.AStar_evaluation = self.heuristic + self.cost

        return( self.greedy_evaluation, self.AStar_evaluation)
    
    
    @staticmethod
    
    # Hàm trả về các bước di chuyển có thể thực hiện từ vị trí hiện tại
    def available_moves(x, n):
        moves = ['L', 'R', 'U', 'D']
        if x % n == 0:
            moves.remove('L')
        if x % n == n - 1:
            moves.remove('R')
        if x - n < 0:
            moves.remove('U')
        if x + n > n * n - 1:
            moves.remove('D')
        
        return moves
    
    # Sinh ra các trạng thái con từ trạng thái hiện tại
    def expand(self, n):
        x = self.state.index(0)
        moves = self.available_moves(x, n)
        
        children = []
        for direction in moves:
            temp = self.state.copy()
            if direction == 'L':
                temp[x], temp[x - 1] = temp[x - 1], temp[x]
            elif direction == 'R':
                temp[x], temp[x + 1] = temp[x + 1], temp[x]
            elif direction == 'U':
                temp[x], temp[x - n] = temp[x - n], temp[x]
            elif direction == 'D':
                temp[x], temp[x + n] = temp[x + n], temp[x]
                
            children.append(State(temp, self, direction, self.depth + 1, 1))
        
        return children

    def solution(self):
        solution = []
        solution.append(self.direction)
        path = self
        while path.parent:
            path = path.parent
            solution.append(path.direction)
        solution = solution[:-1]
        solution.reverse()
        return solution
    
    def states(self):
        states = []
        states.append(self.state)
        path = self
        while path.parent:
            path = path.parent
            states.append(path.state)
        states.reverse()
        return states