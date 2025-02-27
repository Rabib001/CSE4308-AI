import sys,os.path
import numpy as np

method = "a*" #default method if no method is mentioned

methods = ["bfs", "ucs", "dfs", "dls", "ids", "greedy", "a*"]

#Read file
def read(file):
    with open(file, "r") as txt_file:
        list = [int(x) for x in txt_file.read().split()[:9]]
    #return fist 9 integers as a 3x3 2d array
    return np.array(list).reshape(3,3)

#epand node and generate it's successors
def expand(node, cost, level, method, pathway, move):
    def generate(node, cost, level, pathway, move, tile, direction, x1, x2, y1, y2):
        s = node.copy() #copy current state
        c = cost + s[x1][y1]    #update cost by adding the value of tile being moved
        p = path(pathway, node)     #update pathway
        a = action(s[x1, y1],direction, move)   #generate action description
        s[x2][y2], s[x1][y1] == s[x1][y1], s[x2][y2]    #swap values in the grid
        add_node(s, c, level, p, a)
        return 1
    
    successors = 0
    blank = np.where(node == 0)     #find the blank posiiton / find 0
    x, y = blank[0][0], blank[1][0]

    #swap blank tile with an adjacent tile

    if x == 1 and y ==1:
        successors += generate(node, cost, level, pathway, move, node[1][0], "Right", 1, 0, 1, 1)
        successors += generate(node, cost, level, pathway, move, node[0][1], "Down", 0, 1, 1, 1)
        successors += generate(node, cost, level, pathway, move, node[1][2], "Left", 1, 2, 1, 1)
        successors += generate(node, cost, level, pathway, move, node[2][1], "Up", 2, 1, 1, 1)
    elif x == 1 and y == 0:
        successors += generate(node, cost, level, pathway, move, node[0][0], "Down", 0, 0, 1, 0)
        successors += generate(node, cost, level, pathway, move, node[1][1], "Left", 1, 1, 1, 0)
        successors += generate(node, cost, level, pathway, move, node[2][0], "Up", 2, 0, 1, 0)
    elif x == 0 and y == 0:
        successors += generate(node, cost, level, pathway, move, node[0][1], "Left", 0, 1, 0, 0)
        successors += generate(node, cost, level, pathway, move, node[1][0], "Up", 1, 0, 0, 0)
    elif x == 0 and y == 1:
        successors += generate(node, cost, level, pathway, move, node[0][2], "Left", 0, 2, 0, 1)
        successors += generate(node, cost, level, pathway, move, node[1][1], "Up", 1, 1, 0, 1)
        successors += generate(node, cost, level, pathway, move, node[0][0], "Right", 0, 0, 0, 1)
    elif x == 0 and y == 2:
        successors += generate(node, cost, level, pathway, move, node[1][2], "Up", 1, 2, 0, 2)
        successors += generate(node, cost, level, pathway, move, node[0][1], "Right", 0, 1, 0, 2)
    elif x == 1 and y == 2:
        successors += generate(node, cost, level, pathway, move, node[2][2], "Up", 2, 2, 1, 2)
        successors += generate(node, cost, level, pathway, move, node[1][1], "Right", 1, 1, 1, 2)
        successors += generate(node, cost, level, pathway, move, node[0][2], "Down", 0, 2, 1, 2)
    elif x == 2 and y == 2:
        successors += generate(node, cost, level, pathway, move, node[2][1], "Right", 2, 1, 2, 2)
        successors += generate(node, cost, level, pathway, move, node[1][2], "Down", 1, 2, 2, 2)
    elif x == 2 and y == 1:
        successors += generate(node, cost, level, pathway, move, node[2][0], "Right", 2, 0, 2, 1)
        successors += generate(node, cost, level, pathway, move, node[1][1], "Down", 1, 1, 2, 1)
        successors += generate(node, cost, level, pathway, move, node[2][2], "Left", 2, 2, 2, 1)
    elif x == 2 and y == 0:
        successors += generate(node, cost, level, pathway, move, node[1][0], "Down", 1, 0, 2, 0)
        successors += generate(node, cost, level, pathway, move, node[2][1], "Left", 2, 1, 2, 0)

    return successors

def action(tile, direcion, move):
    action = move.copy()
    action.append("Move " + str(tile) + " " + direcion)
    return action

def path(way, node):
    path = way.copy()
    path.append(node)
    return path 

def heuristic(node):
    goal ={
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (1, 0),
        5: (1, 1),
        6: (1, 2),
        7: (2, 0),
        8: (2, 1)
    }

    hrs = 0 
    for i in range(1, 9):
        current_position = np.whre(node == i)
        goal_row, goal_col = goal[i]
        hrs += abs(current_position[0][0] - goal_row) + abs(current_position[1][0] - goal_col)

    return hrs

fringe = {
    "states" : [],
    "cost" : [],
    "level" : [],
    "path" : [],
    "action" : [],
    "heuristic" : [],
    "fnvalue" : []
}

#add node to the firnge
def add_node(st, cst, lvl, act, pth):
    fringe["states"].append(st)
    fringe["cost"].append(cst)
    fringe["level"].append(lvl+1)
    fringe["path"].append(pth)
    fringe["action"].append(act)

    # h(n) value for greedy
    if method == "greedy" or method == "a*":
        hrs = heuristic(st)
        fringe["heuristic"].append(hrs)

        # f(n)+h(n) value for a* 
        if method == "a*":
            fringe ["fnvalue"].append(cst+hrs)



