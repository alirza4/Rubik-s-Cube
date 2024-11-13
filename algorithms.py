import heapq
from collections import OrderedDict, deque

import numpy as np
from location import next_location, solved_location

from state import solved_state
from state import next_state

goal_state = [
    [1, 1],
    [1, 1],
    [2, 2],
    [2, 2],
    [3, 3],
    [3, 3],
    [4, 4],
    [4, 4],
    [5, 5],
    [5, 5],
    [6, 6],
    [6, 6],
]
actions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def solve(init_state, init_location, method):
    """
    Solves the given Rubik's cube using the selected search algorithm.
 
    Args:
        init_state (numpy.array): Initial state of the Rubik's cube.
        init_location (numpy.array): Initial location of the little cubes.
        method (str): Name of the search algorithm.
 
    Returns:
        list: The sequence of actions needed to solve the Rubik's cube.
    """

    # instructions and hints:
    # 1. use 'solved_state()' to obtain the goal state.
    # 2. use 'next_state()' to obtain the next state when taking an action .
    # 3. use 'next_location()' to obtain the next location of the little cubes when taking an action.
    # 4. you can use 'Set', 'Dictionary', 'OrderedDict', and 'heapq' as efficient data structures.

    if method == 'Random':
        return list(np.random.randint(1, 12 + 1, 10))

    elif method == 'IDS-DFS':
        return IDDFS(init_state, 100)
    elif method == 'A*':
        return Astar(init_state, init_location)
    elif method == 'BiBFS':
        return BIBFS(init_state)

    else:
        return []


def IDDFS(init_state, maxDepth=15):
    for depth in range(1, maxDepth):
        key = tuple(map(tuple, init_state))
        frontier = OrderedDict()
        frontier[key] = []
        explored = 0
        expand = 0
        while frontier:
            currentState, currentValue = [list(t) for t in frontier.popitem()]
            explored = explored + 1
            if tuple(map(tuple, currentState)) == tuple(map(tuple, solved_state())):
                print(depth)
                print(explored)
                print(expand)
                return currentValue
            if depth > len(currentValue):
                for action in actions:
                    child_state = tuple(map(tuple, next_state(currentState, int(action))))
                    expand = expand + 1
                    if child_state not in frontier:
                        frontier[child_state] = currentValue + [action]
    return None


def manhattanHeuristic(current):
    heuristic = 0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                value = current[i][j][k]
                position = goalPosition(value)
                if position is None:
                    return None
                heuristic += abs(i - position[0]) + abs(j - position[1]) + abs(k - position[2])
    return int(heuristic / 4)


def goalPosition(value):
    indices = np.where(solved_location() == value)
    if len(indices[0]) == 0:
        return None
    return tuple(indices)

def Astar(initialState, initialLocation):
    h = manhattanHeuristic(initialLocation)
    frontier = []
    heapq.heappush(frontier, (h, initialState, initialLocation, []))
    exploredCount = 0
    expandedCount = 0
    explored = set()
    while frontier:
        currentCost, currentState, currentLocation, currentActions = heapq.heappop(frontier)
        explored.add(str(currentState))
        exploredCount = exploredCount + 1
        for action in actions:
            nextLocation = next_location(currentLocation, action)
            nextState = next_state(currentState, action)
            nextStatusTuple = tuple(map(tuple, nextState))
            expandedCount = expandedCount + 1
            if nextStatusTuple not in explored:
                h = manhattanHeuristic(nextLocation)
                newCost = currentCost + 1
                newActions = currentActions + [action]
                heapq.heappush(frontier, (newCost + h, nextStatusTuple, nextLocation, newActions))
                if tuple(map(tuple, nextState)) == tuple(map(tuple, solved_state())):
                    print(exploredCount)
                    print(expandedCount)
                    return newActions
                explored.add(nextStatusTuple)
    return None


def BIBFS(init_state):
    startQueue = deque([(init_state, [])])
    goalQueue = deque([(solved_state(), [])])
    startExplored = {tuple(map(tuple, init_state))}
    goal_explored = {tuple(map(tuple, solved_state())): None}
    explored = 0
    expanded = 0

    while startQueue and goalQueue:
        currentState, currentActions = startQueue.popleft()
        goalState, goalActions = goalQueue.popleft()
        start_state_tuple = tuple(map(tuple, currentState))
        if start_state_tuple in goal_explored:
            succedActions = []
            for action in goal_explored[start_state_tuple][::-1]:
                succedActions = succedActions + [reverseAction(action)]
            print(explored)
            print(expanded)
            return currentActions + succedActions

        explored = explored + 1
        for action in actions:
            expanded = expanded + 1
            newState = next_state(currentState, action)
            newStateTuple = tuple(map(tuple, newState))
            if newStateTuple not in startExplored:
                startQueue.append((newState, currentActions + [action]))
                startExplored.add(newStateTuple)

            expanded = expanded + 1
            newGoalState = next_state(goalState, action)
            newGoalStateTuple = tuple(map(tuple, newGoalState))
            if newGoalStateTuple not in goal_explored:
                goalQueue.append((newGoalState, goalActions + [action]))
                goal_explored[newGoalStateTuple] = currentActions + [action]

    return None


def reverseAction(action):
    newAction = None
    match action:
        case 1:
            newAction = 7
        case 2:
            newAction = 8
        case 3:
            newAction = 9
        case 4:
            newAction = 10
        case 5:
            newAction = 11
        case 6:
            newAction = 12
        case 7:
            newAction = 1
        case 8:
            newAction = 2
        case 9:
            newAction = 3
        case 10:
            newAction = 4
        case 11:
            newAction = 5
        case 12:
            newAction = 6
    return newAction
