# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from queue import PriorityQueue
from game import Directions
from game import Actions
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    from game import Directions
    print ("Start:", problem.getStartState())
    print ("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print ("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    path = dfs_search((problem.getStartState(), '', 0), problem, [], list())
    solution = [pos[1] for pos in path[1:]]
    return solution
    
def dfs_search(state, problem, path, explored):
    path.append(state)
    explored.append(state)
    #print("  path: " + str([p for p in path]))
    
    if problem.isGoalState(state[0]):
        print("  => Found goal!")
        return path
    
    for child in problem.getSuccessors(state[0]):
        if child[0] in [pos[0] for pos in explored]:
            continue
        result = dfs_search(child, problem, path.copy(), explored)
        if result:
            return result
        
    #print("Leaving {}".format(state))
    return False;

def breadthFirstSearch(problem):
        
    states = PriorityQueue()
    states.put((1, [(problem.getStartState(), '', 0)]))#State, Action, Cost
    explored = []
    frontier = [problem.getStartState()]
    while True:
        #print("  -------------")
        #print("  frontier: " + str([p for p in frontier]))
        #print("  explored: " + str([p for p in explored]))
        if len(frontier) == 0:
            return False
        statePath = states.get()[1]
        state = statePath[-1]
        
        #print("  Will expand state: " + str(state))
        frontier.remove(state[0])
        explored.append(state[0])
        if problem.isGoalState(state[0]):
            print("  => Found goal!")
            print([p[1] for p in statePath[1:]])
            return [p[1] for p in statePath[1:]]
        for successor in problem.getSuccessors(state[0]):
            if successor[0] not in frontier and successor[0] not in explored:
                statePathNew = statePath.copy()
                statePathNew.append(successor)
                states.put((len(statePathNew), statePathNew))
                frontier.append(successor[0])

def uniformCostSearch(problem):
    
    states = PriorityQueue()
    states.put((1, [(problem.getStartState(), '', 0)]))#State, Action, Cost
    explored = []
    frontier = [problem.getStartState()]
    while True:
        #print("  -------------")
        #print("  frontier: " + str([p for p in frontier]))
        #print("  explored: " + str([p for p in explored]))
        if len(frontier) == 0:
            return False
        statePath = states.get()[1]
        state = statePath[-1]
        
        #print("  Will expand state: " + str(state))
        frontier.remove(state[0])
        explored.append(state[0])
        if problem.isGoalState(state[0]):
            print("  => Found goal!")
            print([p[1] for p in statePath[1:]])
            return [p[1] for p in statePath[1:]]
        for successor in problem.getSuccessors(state[0]):
            if successor[0] not in frontier and successor[0] not in explored:
                statePathNew = statePath.copy()
                statePathNew.append(successor)
                cost = sum([successor[2] for successor in statePathNew])
                states.put((cost, statePathNew))
                frontier.append(successor[0])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    states = PriorityQueue()
    states.put((1, [(problem.getStartState(), '', 0)]))#State, Action, Cost
    explored = []
    frontier = [problem.getStartState()]
    while True:
        #print("  ############ -------------")
        #print("  frontier: " + str([p for p in frontier]))
        #print("  explored: " + str([p for p in explored]))
        if len(frontier) == 0:
            return False
        statePath = states.get()[1]
        state = statePath[-1]
        
        #print("  Will expand state: " + str(state))
        frontier.remove(state[0])
        explored.append(state[0])
        if problem.isGoalState(state[0]):
            print("  => Found goal!")
            print ([p[1] for p in statePath[1:]])
            return [p[1] for p in statePath[1:]]
        for successor in problem.getSuccessors(state[0]):
            if successor[0] not in frontier and successor[0] not in explored:
                statePathNew = statePath.copy()
                statePathNew.append(successor)
                estimate = heuristic(successor[0], problem)
                cost = sum([successor[2] for successor in statePathNew])
                states.put((cost + estimate, statePathNew))
                frontier.append(successor[0])

def getDirectionsFromTuple(tuples):
    result = []
    for i in range(len(tuples)-2):
        x1,y1 = tuples[i+1]
        x0,y0 = tuples[i]
        result.append(Actions.vectorToDirection((x1-x0, y1-y0)))
    return result

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
