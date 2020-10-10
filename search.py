# coding=utf-8
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
    return [s, s, w, s, w, w, s, w]


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
    "*** YOUR CODE HERE ***"
    # initializing node and getting start state
    node = {'state': problem.getStartState(), 'actions':[], 'cost':0}
    # check whether the state is a goal state or not
    if problem.isGoalState(node['state']):
        return []
    # initialize frontier stack
    frontier = util.Stack()
    # to store explored nodes
    explored = []
    # pushing the nodes into stack
    frontier.push((node['state'], node['actions']))
    while not frontier.isEmpty():
        current_node = frontier.pop()
        # if the present node is not in explored then add it to explored
        if current_node[0] not in explored:
            explored.append(current_node[0])

            # if the current state is goal state then return the actions applied till now stored in current_node[1]
            if problem.isGoalState(current_node[0]):
                return current_node[1]

            # get the child nodes and apply the same process through the while loop till the goal state is reached
            successors = problem.getSuccessors(current_node[0])
            for successor in successors:
                new_action = current_node[1] + [successor[1]]
                frontier.push((successor[0], new_action))



def breadthFirstSearch(problem):
    # initialize the node
    node = {'state': problem.getStartState(), 'cost': 0}

    # check weather the state is the goal state or not
    if problem.isGoalState(node['state']):
        return []

    # initialize the frontier queue
    frontier = util.Queue()

    # loading the current state to the frontier queue
    frontier.push(node)

    # initiailize the explored list to store the explored nodes
    explored = []

    # initializing the frontier set to store all the states which are loaded to the frontier queue
    frontierSet = []

    while True:
        if frontier.isEmpty():
            raise Exception('Search Failed!')

        # popping the first in node
        node = frontier.pop()

        # when the goal state is reached
        if problem.isGoalState(node['state']):
            actions = []

            # retracing the path using the parent node which we stored in the node set
            # till we do not have any parent node i.e., till the initial state is reached
            while 'parent' in node:
                actions.append(node['action'])
                node = node['parent']

            # as we have traversed from goal state to initial state while appending the actions,
            # we need to reverse the list of action to get the correct of action to be applied
            actions.reverse()
            return actions
        explored.append(node['state'])

        # getting successors and continuing the process till the goal state is reached
        frontierSet.append(node['state'])
        successors = problem.getSuccessors(node['state'])
        for successor in successors:
            child = {'state': successor[0], 'action': successor[1], 'cost': successor[2], 'parent': node}
            if child['state'] not in frontierSet:
                frontier.push(child)
                frontierSet.append(child['state'])



def uniformCostSearch(problem):
    # initializing the node and checking if the start is the goal state
    node = problem.getStartState()
    if problem.isGoalState(node):
        return []

    # initializing the frontier as priority queue
    frontier_priority_queue = util.PriorityQueue()
    frontier_priority_queue.push((node, [], 0), 0)
    # initializing the explored set to store the explored nodes
    explored = set()
    while True:
        if frontier_priority_queue.isEmpty():
            raise Exception('Search Failed')

        # popping the least priority node and checking weather it is a goal state or not
        node = frontier_priority_queue.pop()
        if node[0] not in explored:
            explored.add(node[0])
            if problem.isGoalState(node[0]):
                return node[1]

            # getting the successors and continuing the loop
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                new_action = node[1] + [successor[1]]
                priority = node[2] + successor[2]
                frontier_priority_queue.push((successor[0], new_action, priority), priority)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # initializing the node and checking if the start is the goal state
    node = problem.getStartState()
    if problem.isGoalState(node):
        return []

    # initializing the frontier as priority queue
    frontier_priority_queue = util.PriorityQueue()
    frontier_priority_queue.push((node, [], 0), 0)
    explored = []

    while True:
        if frontier_priority_queue.isEmpty():
            raise Exception('Search Failed')

        # popping the least priority node and checking weather it is a goal state or not
        node = frontier_priority_queue.pop()
        if node[0] not in explored:
            explored.append(node[0])

            if problem.isGoalState(node[0]):
                return node[1]

            # loading the next states along the heuristic values into the priority queue
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                new_action = node[1] + [successor[1]]
                total_cost = node[2] + successor[2]
                heuristic_cost = total_cost + heuristic(successor[0], problem)
                frontier_priority_queue.push((successor[0], new_action, total_cost), heuristic_cost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
