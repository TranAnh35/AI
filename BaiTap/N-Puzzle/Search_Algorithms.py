from State import State
from queue import PriorityQueue

#Breadth-first Search
def BFS(given_state , n):
    root = State(given_state, None, None, 0, 0)
    if root.isGoal():
        return root.states(), root.solution(), 0
    frontier = [root]
    explored = set()
    
    while frontier:
        current_node = frontier.pop(0)
        explored.add(tuple(current_node.state))
        
        children = current_node.expand(n)
        for child in children:
            if tuple(child.state) not in explored:
                if child.isGoal():
                    return child.states(), child.solution(), len(explored)
                frontier.append(child)
    return

#Depth-first Search with limited depth
def DFS(given_state , n, depth): 
    limit = 30 if depth == 0 else depth
    root = State(given_state, None, None, depth, 0)
    if root.isGoal():
        return root.states(), root.solution(), 0
    frontier = [root]
    explored = set()
    
    while not(frontier.__len__() == 0):
        current_node = frontier.pop(frontier.__len__() - 1)
        max_depth = current_node.depth # Dộ sâu hiện tại
        explored.add(tuple(current_node.state))
        
        if max_depth == limit:
            continue # Đi đến nhánh tiếp theo

        children = current_node.expand(n)
        for child in children:
            if tuple(child.state) not in explored:
                if child.isGoal():
                    return child.states(), child.solution(), len(explored)
                frontier.append(child)
    return (("Couldn't find solution in the limited depth."), len(explored))
        
    
    
def Greedy(given_state , n):
    frontier = PriorityQueue()
    explored = []
    counter = 0
    root = State(given_state, None, None, 0, 0)
    evaluation = root.Manhattan_Distance(n) # Có thể sử dụng Misplaced_Tiles() để thay thế.
    frontier.put((evaluation[0], counter, root)) # Dựa trên đánh giá Greedy

    while not frontier.empty():
        current_node = frontier.get()
        current_node = current_node[2]
        explored.append(current_node.state)
        
        if current_node.isGoal():
            return current_node.states(), current_node.solution(), len(explored)

        children = current_node.expand(n)
        for child in children:
            if child.state not in explored:
                counter += 1
                evaluation = child.Manhattan_Distance(n) # Có thể sử dụng Misplaced_Tiles() để thay thế.
                frontier.put((evaluation[0], counter, child)) # Dựa trên đánh giá Greedy
    return


def AStar_search(given_state , n):
    frontier = PriorityQueue()
    explored = []
    counter = 0
    root = State(given_state, None, None, 0, 0)
    evaluation = root.Manhattan_Distance(n) # Có thể sử dụng Misplaced_Tiles() để thay thế.
    frontier.put((evaluation[1], counter, root)) # Dựa trên đánh giá A*

    while not frontier.empty():
        current_node = frontier.get()
        current_node = current_node[2]
        explored.append(current_node.state)
        
        if current_node.isGoal():
            return current_node.states(), current_node.solution(), len(explored)

        children = current_node.expand(n)
        for child in children:
            if child.state not in explored:
                counter += 1
                evaluation = child.Manhattan_Distance(n) # Có thể sử dụng Misplaced_Tiles() để thay thế.
                frontier.put((evaluation[1], counter, child)) # Dựa trên đánh giá A*
    return