from collections import deque
from queue import Queue
from threading import Lock
import threading
import time
import timeit
import heapq
import math

# ----------------------------Tree Nodes-------------------------------------
class Node:
    def __init__(self, state, parent, dirMoved, depth, cost, key):
        self.state = state
        self.parent = parent
        self.dirMoved = dirMoved
        self.depth = depth
        self.cost = cost
        self.key = key

        def __eq__(self, other):
            return self.state is other.state

        def __str__(self):
            return str(self.state)

        def __getDepth__(Node):
            return self.depth

# ----------------------------Global Variables-------------------------------------
goalState = '012345678'
NodesExp = 0
maxSearchDepth = 0
# -----------------------------Heuristic Functions_____________________________________
def heuristicMan(initial_state):
    h = 0
    for i, item in enumerate(initial_state):
        prev_row, prev_col = i // 3, i % 3
        goal_row, goal_col = int(item) // 3, int(item) % 3
        h += abs(prev_row - goal_row) + abs(prev_col - goal_col)
    return h


def heuristicEc(initial_state):
    h = 0
    for i, item in enumerate(initial_state):
        prev_row, prev_col = i // 3, i % 3
        goal_row, goal_col = int(item) // 3, int(item) % 3
        h += math.sqrt(math.pow(prev_row - goal_row, 2)+ math.pow(prev_col - goal_col,2))
    return h

# _____________________________Is Solvable Function______________________________________
def isSolvable(initState):
    inv_count = 0
    empty_value = '0'
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if initState[j] != empty_value and initState[i] != empty_value and initState[i] > initState[j]:
                inv_count += 1
    if  inv_count % 2 == 0: return True
    else: return False


# ----------------------------Traversal Functions-------------------------------------
def swapTiles(state, tile1, tile2):
    i = state.find(tile1)
    j = state.find(tile2)
    state = list(state)
    state[i], state[j] = state[j], state[i]
    return ''.join(state)

def getAdj(i):
    if i == -1: return -1
    if i == 4:
        return [1, 3, 5, 7]
    elif i == 0:
        return [-1, -1, 1, 3]
    elif i == 2:
        return [-1, 1, -1, 5]
    elif i == 6:
        return [3, -1, 7, -1]
    elif i == 8:
        return [5, 7, -1, -1]
    elif i == 1:
        return [-1, 0, 2, 4]
    elif i == 3:
        return [0, -1, 4, 6]
    elif i == 5:
        return [2, 4, -1, 8]
    elif i == 7:
        return [4, 6, 8, -1]

def getChildStates(node):
    global NodesExp
    NodesExp = NodesExp + 1
    children = list()
    adjacent = getAdj(node.state.find('0'))
    if adjacent == -1: return -1
    for n, i in enumerate(adjacent):
        if i != -1:
            newState = swapTiles(node.state,'0',node.state[i])
            children.append(Node(newState,node,n,node.depth+1,node.cost+1,0))
    return children

def getPath(initialState,node):
    moves = []
    while node.state != initialState:
        if node.dirMoved == 0:
            path = 'Up'
        if node.dirMoved == 1:
            path = 'Left'
        if node.dirMoved == 2:
            path = 'Right'
        if node.dirMoved == 3:
            path = 'Down'
        moves.insert(0, path)
        node = node.parent
    return moves

# ----------------------------BFS Search-------------------------------------
def bfsSearch(initialState):
    # create a set for the explored and a queue containing the frontier states
    global goalState, maxSearchDepth
    explored = set()
    frontier = Queue()
    frontier.put(Node(initialState,None,None,0,0,0))
    # iterate over frontier until goal is found or the tree is exhausted
    while not frontier.empty():
        node = frontier.get()
        explored.add(node)  # start exploring current state
        if node.state == goalState:
            return node
        children = getChildStates(node)
        for child in children:
            if child.state not in explored:
                frontier.put(child)
                explored.add(child.state)
                if child.depth > maxSearchDepth:
                    maxSearchDepth = maxSearchDepth + 1
    return 'goal not found'
# ----------------------------DFS Search-------------------------------------
def dfsSearch(initialState):
    global goalState, maxSearchDepth
    frontier = [Node(initialState, None, None, 0, 0, 0)]
    explored = set()
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        if node.state == goalState: 
            return node

        paths = reversed(getChildStates(node))
        for neighbor in paths:
            if neighbor.state not in explored:
                if neighbor not in frontier:
                    frontier.append(neighbor)
                    explored.add(neighbor.state)
                    if neighbor.depth > maxSearchDepth:
                        maxSearchDepth = maxSearchDepth + 1
    
    return 'goal not found'

# ------------------------A* Manhattan---------------------------------
def aStarMan(initialState):
    global goalState, maxSearchDepth
    frontier = [Node(initialState, None, None, 0, 0, heuristicMan(initialState))]
    explored = set()
    while frontier:
        frontier.sort(key=lambda o: o.key)
        node = frontier.pop(0)
        explored.add(node.state)
        if node.state == goalState:
            return node
        for neighbor in getChildStates(node):
            neighbor.key = neighbor.depth + heuristicMan(neighbor.state)
            if neighbor.state not in explored:
                if neighbor not in frontier:
                    frontier.append(neighbor)
                    if neighbor.depth > maxSearchDepth:
                        maxSearchDepth = maxSearchDepth + 1
                elif neighbor in frontier:
                    index = frontier.index(neighbor)
                    if neighbor.key < frontier[index].key:
                        frontier.remove(index)
                        frontier.append(neighbor)

    return 'goal not found'
# ------------------------A* Euclidean---------------------------------
def aStarEc(initialState):
    global goalState, maxSearchDepth
    frontier = [Node(initialState, None, None, 0, 0, heuristicEc(initialState))]
    explored = set()
    while frontier:
        frontier.sort(key=lambda o: o.key)
        node = frontier.pop(0)
        explored.add(node.state)
        if node.state == goalState:
            return node
        for neighbor in getChildStates(node):
            neighbor.key = neighbor.depth + heuristicEc(neighbor.state)
            if neighbor.state not in explored:
                if neighbor not in frontier:
                    frontier.append(neighbor)
                    if neighbor.depth > maxSearchDepth:
                        maxSearchDepth = maxSearchDepth + 1
                elif neighbor in frontier:
                    index = frontier.index(neighbor)
                    if neighbor.key < frontier[index].key:
                        frontier.remove(index)
                        frontier.append(neighbor)

    return 'goal not found'
# ----------------------------MAIN-------------------------------------

def main(initState, searchAlg):
    global maxSearchDepth, NodesExp
    NodesExp = 0
    maxSearchDepth = 0
    algorithms = {
        'BFS': bfsSearch,
        'DFS': dfsSearch,
        'A* (Manhattan)': aStarMan,
        'A* (Euclidean)': aStarEc,

    }

    start = timeit.default_timer()
    endState = algorithms.get(searchAlg)(initState)
    stop = timeit.default_timer()

    if endState == 'goal not found':
        return 'goal not found'
    pathTaken = getPath(initState, endState)
    runtime = stop-start
    print(endState.cost)
    print(NodesExp)
    return ([endState,pathTaken,NodesExp,runtime,maxSearchDepth])