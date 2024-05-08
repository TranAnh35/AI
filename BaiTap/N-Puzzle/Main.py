from Search_Algorithms import BFS, DFS, Greedy, AStar_search

def print_puzzle(puzzle):
    if not puzzle:
        return
    for i in range(0,n*n):
        print(puzzle[i] , end = " ")
        if (i+1) % n == 0:
            print()
    print()
    
#initial state
n = int(input("Enter n\n"))
print("Enter your" ,n,"*",n, "puzzle")
root = []
# for i in range(0,n*n):
#     p = int(input())
#     root.append(p)

root = [int(num) for num in input().split()]

print("The given state is:\n")
print_puzzle(root)

#đếm số lần đảo ngược     
def inv_num(puzzle):
    inv = 0
    for i in range(len(puzzle)):
        for j in range(i+1 , len(puzzle)):
            if (( puzzle[i] > puzzle[j]) and puzzle[i] and puzzle[j]):
                inv += 1
    return inv

def isValid(puzzle):
    if len(puzzle) != len(set(puzzle)) or 0 not in puzzle:
        return False
    
    for i in range(len(puzzle)):
        row, col = divmod(i, n)
        value = puzzle[i]
        if value != 0:
            if puzzle[row * n: (row + 1) * n].count(value) > 1:
                return False
            if [puzzle[j] for j in range(col, len(puzzle), n)].count(value) > 1:
                return False
    return True

def solvable(puzzle): # kiểm tra xem câu đố trạng thái ban đầu có thể giải được hay không: số lần đảo ngược phải là số chẵn.
    if not isValid(puzzle):
        return False
    inv_counter = inv_num(puzzle)
    row = puzzle.index(0) // n
    distance = n - row - 1
    if ((inv_counter + distance) % 2 ==0):
        return True
    return False


from time import time

if AStar_search(root, n):
    while 1:
        verbose = input("Do you want to see the steps? (y/n): ")
        if verbose == 'y':
            verbose = True
            break
        elif verbose == 'n':
            verbose = False
            break
        else:
            print("Invalid input. Please try again.")
    depth = int(input("Enter the depth limit for DFS: "))
    print("Solving, wait a minute\n")
    
    time1 = time()
    BFS_solution = BFS(root, n)
    BFS_time = time() - time1
    print('BFS Solution :')
    if verbose:
        print('States: ')
        for i in range(len(BFS_solution[0])):
            print_puzzle(BFS_solution[0][i])
    print('Path ',BFS_solution[1].__len__(), "\n", BFS_solution[1])
    print('Number of explored nodes is ', BFS_solution[2])    
    print('BFS Time:', BFS_time , "\n")
    
    time2 = time()
    DFS_solution = DFS(root, n, depth)
    DFS_time = time() - time2
    print('DFS Solution : ')
    if DFS_solution[0] == "Couldn't find solution in the limited depth.":
        print(DFS_solution[0], '\n')
    else:
        if verbose:
            print('States: ')
            for i in range(len(DFS_solution[0])):
                print_puzzle(DFS_solution[0][i])
        print('Path ', len(DFS_solution[1]), "\n" , DFS_solution[1])
        print('Number of explored nodes is ', DFS_solution[2])
        print('DFS Time:', DFS_time, "\n")  
    
    time3 = time()
    Greedy_solution = Greedy(root, n)
    Greedy_time = time() - time3
    print('Greedy Solution : ')
    if verbose:
        print('States: ')
        for i in range(len(Greedy_solution[0])):
            print_puzzle(Greedy_solution[0][i])
    print('Path ', len(Greedy_solution[1]), '\n', Greedy_solution[1])
    print('Number of explored nodes is ', Greedy_solution[2])   
    print('Greedy Time:', Greedy_time , "\n")
    
    time4 = time()
    AStar_solution = AStar_search(root, n)
    AStar_time = time() - time4
    print('A* Solution : ')
    if verbose:
        print('States: ')
        for i in range(len(AStar_solution[0])):
            print_puzzle(AStar_solution[0][i])
    print('Path ', len(AStar_solution[1]), '\n', AStar_solution[1])
    print('Number of explored nodes is ', AStar_solution[2])   
    print('A* Time:', AStar_time)
    
    
else:
    print("Not solvable")