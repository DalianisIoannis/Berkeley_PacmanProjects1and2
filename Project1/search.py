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
    return  [s, s, w, s, w, w, s, w]

def DFS_BFS(problem,data_structure):#used for implementing DFS and BFS
    have_visited=dict() #dictionary of nodes i have visited
    f=1 #cost of movement
    first_node = problem.getStartState()
    data_structure.push(  (first_node, list(), f)  )
    #in the beginning list of actions is empty
    while not data_structure.isEmpty():
        node_popped=data_structure.pop()
        if problem.isGoalState(node_popped[0]): #have i found node i am loooking for?
            return node_popped[1]    #return total movements for reaching node
        if node_popped[0] not in have_visited:
            have_visited[ node_popped[0] ]="Visited"
            for adjacent_node in problem.getSuccessors(node_popped[0]): #put all successors in data_structure
                if adjacent_node[0]:    #not_empty
                    if adjacent_node[0] not in have_visited:
                        temp_list=list() #for returning all movements
                        for move_action in node_popped[1]:    #new node will have the total actions for reaching itself
                            temp_list.append(move_action)
                        temp_list.append(adjacent_node[1])  #plus its own final action
                        data_structure.push( [adjacent_node[0] , temp_list] )
    return None #no result

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
    my_stack = util.Stack() #DFS works with the logic of a stack
    return DFS_BFS(problem,my_stack)
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    my_queue = util.Queue() #BFS works with the logic of a queue
    return DFS_BFS(problem,my_queue)
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def Implementation_withPQ(problem, heuristic=nullHeuristic):
    # the priority queue brings out the item with least priority
    # the item i give to P_Q is e.g. (((5,5),"West",1))
    my_PQ=util.PriorityQueue()  #open_list for aStarSearch
    have_visited=dict() #closed_list for aStarSearch
    f=0 #first cost is 0 as is first priority
    item_no_one = (problem.getStartState() ,list() , f)
    my_PQ.update(item_no_one , f)
    while not my_PQ.isEmpty():
        #node_popped is node q for aStarSearch
        node_popped=my_PQ.pop() #take node with smallest priority
        if problem.isGoalState(node_popped[0]): 
            return node_popped[1]
        if node_popped[0] not in have_visited: #check only successors of not visited
            have_visited[ node_popped[0] ]="Visited"
            for adjacent_node in problem.getSuccessors(node_popped[0]):
                if adjacent_node[0]:    #not_empty
                    if adjacent_node[0] not in have_visited:
                        temp_list=list()    #used to store all movements+the last one
                        new_weight=node_popped[2]+adjacent_node[2]
                        #new_weight is cost of popped+cost of child
                        #new_weight is value g for aStarSearch
                        new_h=heuristic( adjacent_node[0],problem ) #used for aStarSearch only
                        new_f = new_weight+new_h
                        #in aStarSearch f=g+h
                        for i in node_popped[1]:
                            temp_list.append(i)
                        temp_list.append(adjacent_node[1])
                        my_PQ.update( (adjacent_node[0],temp_list,new_weight),new_f ) 
    return None #no result

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return Implementation_withPQ(problem)
    # util.raiseNotDefined()

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # algorithm studied from https://www.geeksforgeeks.org/a-search-algorithm/
    # value f=g+h
    # g cost of movements to current node
    # h:heuristic
    # closed_list=dict()
    # open_list=util.PriorityQueue()
    # f=0
    # item_no_one = (problem.getStartState() ,list() , f)
    # open_list.push( item_no_one,f )
    return Implementation_withPQ(problem, heuristic)
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
