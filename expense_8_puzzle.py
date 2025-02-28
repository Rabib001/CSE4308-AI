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
    def generate(node, cost, level, pathway, move, tile, direction, x1, y1, x2, y2):
        s = node.copy() #copy current state
        c = cost + s[x1][y1]    #update cost by adding the value of tile being moved
        p = path(pathway, node)     #update pathway
        a = action(s[x1, y1],direction, move)   #generate action description
        s[x2][y2], s[x1][y1] = s[x1][y1], s[x2][y2]    #swap values in the grid
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


def calculate_hrs(node):
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
        current_position = np.where(node == i)
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
def add_node(st, cst, lvl, pth, act):
    fringe["states"].append(st)
    fringe["cost"].append(cst)
    fringe["level"].append(lvl+1)
    fringe["path"].append(pth)
    fringe["action"].append(act)

    if method == "greedy" or method == "a*":
        hrs = calculate_hrs(st)
        fringe["heuristic"].append(hrs) # h(n) value for greedy

        if method == "a*":
            fringe ["fnvalue"].append(cst+hrs)  # f(n)+h(n) value for a* 



num = len(sys.argv)

if os.path.isfile(sys.argv[1]) == 1:
    start = read(sys.argv[1])
else:
    print("Invalid Start file\n")

if os.path.isfile(sys.argv[2]) == 1:
    goal = read(sys.argv[2])
else:
    print("Invalid Goal file\n")

Flag = "false"
args = []

for i in range(len(sys.argv)):
    args.append(sys.argv[i])

if "true" in args:
    Flag = "true"

for arg in args:
    if arg in methods:
        method = arg


if Flag == "true":
    file1 = open("dump.txt","w")
    file1.write("Command-Line Arguments: ")
    file1.write(str(args[1:]))
    file1.write("\nMethod Selected: {}".format(method))
    file1.write("\nRunning {}".format(method))
    file1.close()

i = 0
closed = []
node = start.copy()
fringe["states"].append(node)
fringe["cost"].append(0)
fringe["level"].append(0)
pathway = []
pathway.append(None)
fringe["path"].append(pathway)
move = []
move.append(None)
fringe["action"].append(move)
fringe["heuristic"].append(calculate_hrs(node))
fringe["fnvalue"].append(fringe["cost"][0]+fringe["heuristic"][0])
expanded = 0
popped = 0
generated = 1
fsize = len(fringe["states"])


# Write on dump file
def writeonfile(node, cost, level, pathway, move, successors, fnvalue=None):
    with open("dump.txt", "a") as file1:
        # Write common content
        if method == "a*":
            file1.write(
                f"\nGenerating successors to < state = {node}, action = {move}, g(n) = {cost}, "
                f"d = {level}, f(n) = {fnvalue}, parent = {pathway} >:"
            )
        else:
            file1.write(
                f"\nGenerating successors to < state = {node}, action = {move}, g(n) = {cost}, "
                f"d = {level}, parent = {pathway} >:"
            )

        file1.write(f"\n{successors} successors generated")

        # Write closed list (if applicable)
        if method not in ("ids", "dls"):
            file1.write(f"\nClosed: {closed}")

        # Write fringe content
        file1.write("\nFringe:")
        for i in range(len(fringe["states"])):
            if method == "a*":
                file1.write(
                    f"\n< state = {fringe['states'][i]}, action = {fringe['action'][i][-1]}, "
                    f"g(n) = {fringe['cost'][i]}, d = {fringe['level'][i]}, "
                    f"f(n) = {fringe['fnvalue'][i]}, parent = {fringe['path'][i][-1]} >"
                )
            else:
                file1.write(
                    f"\n< state = {fringe['states'][i]}, action = {fringe['action'][i][-1]}, "
                    f"g(n) = {fringe['cost'][i]}, d = {fringe['level'][i]}, "
                    f"parent = {fringe['path'][i][-1]} >"
                )
    

def writegoalonfile(node, cost, level, pathway, move, fnvalue=None):
    with open("dump.txt", "a") as file1:
        if method == "a*":
            file1.write(
                f"\nGoal state reached: < state = {node}, action = {move}, g(n) = {cost}, "
                f"d = {level}, f(n) = {fnvalue}, parent = {pathway} >:"
            )
        else:
            file1.write(
                f"\nGoal state reached: < state = {node}, action = {move}, g(n) = {cost}, "
                f"d = {level}, parent = {pathway} >:"
            )
        
        file1.write(f"\nNodes Popped: {popped}")
        file1.write(f"\nNodes Expanded: {expanded}")
        file1.write(f"\nMax Fringe Size: {fsize}")

        if method != "a*":
            file1.write(f"\nNodes Generated: {generated}")


if method == 'bfs':
    while fringe["states"]:
        # Pop the first node from the fringe
        node, cost, level, pathway, move = (
            fringe["states"].pop(0),
            fringe["cost"].pop(0),
            fringe["level"].pop(0),
            fringe["path"].pop(0),
            fringe["action"].pop(0)
        )
        popped += 1

        # Check if the goal is reached
        if (node == goal).all():
            print(f"Nodes Popped: {popped}")
            print(f"Nodes Expanded: {expanded}")
            print(f"Nodes Generated: {generated}")
            print(f"Max Fringe Size: {fsize}")
            print(f"Nodes enclosed: {len(closed)}")
            print(f"Goal reached at depth {level} at a cost of {cost}.")
            print("Steps:")
            for step in move[1:]:
                print(step)
            writegoalonfile(node, cost, level, pathway[-1], move[-1])
            break

        # Skip if the node is already in the closed list
        if any((node == x).all() for x in closed):
            continue

        # Generate successors and update fringe
        successors = expand(node, cost, level, method, pathway, move)
        generated += successors
        closed.append(node)
        if Flag == "true":
            writeonfile(node, cost, level, pathway[-1], move[-1], successors)
        expanded += 1

        # Update max fringe size
        fsize = max(fsize, len(fringe["states"]))

if method == 'ucs':
    while fringe["states"]:
        # Find the node with the lowest cost
        lowest_cost_index = fringe["cost"].index(min(fringe["cost"]))
        
        # Pop the node with the lowest cost
        node, cost, level, pathway, move = (
            fringe["states"].pop(lowest_cost_index),
            fringe["cost"].pop(lowest_cost_index),
            fringe["level"].pop(lowest_cost_index),
            fringe["path"].pop(lowest_cost_index),
            fringe["action"].pop(lowest_cost_index)
        )
        popped += 1

        # Check if the goal is reached
        if (node == goal).all():
            print(f"Nodes Popped: {popped}")
            print(f"Nodes Expanded: {expanded}")
            print(f"Nodes Generated: {generated}")
            print(f"Max Fringe Size: {fsize}")
            print(f"Nodes enclosed: {len(closed)}")
            print(f"Goal reached at depth {level} at a cost of {cost}.")
            print("Steps:")
            for step in move[1:]:
                print(step)
            writegoalonfile(node, cost, level, pathway[-1], move[-1])
            break

        # Skip if the node is already in the closed list
        if any((node == x).all() for x in closed):
            continue

        # Generate successors and update fringe
        successors = expand(node, cost, level, method, pathway, move)
        generated += successors
        closed.append(node)
        if Flag == "true":
            writeonfile(node, cost, level, pathway[-1], move[-1], successors)
        expanded += 1

        # Update max fringe size
        fsize = max(fsize, len(fringe["states"]))

if method == "greedy":
    while fringe["states"]:
        # Find the node with the lowest heuristic value
        lowest_heuristic_index = fringe["heuristic"].index(min(fringe["heuristic"]))
        
        # Pop the node with the lowest heuristic value
        node, cost, level, pathway, move, heuristic = (
            fringe["states"].pop(lowest_heuristic_index),
            fringe["cost"].pop(lowest_heuristic_index),
            fringe["level"].pop(lowest_heuristic_index),
            fringe["path"].pop(lowest_heuristic_index),
            fringe["action"].pop(lowest_heuristic_index),
            fringe["heuristic"].pop(lowest_heuristic_index)
        )
        popped += 1

        # Check if the goal is reached
        if (node == goal).all():
            print(f"Nodes Popped: {popped}")
            print(f"Nodes Expanded: {expanded}")
            print(f"Nodes Generated: {generated}")
            print(f"Max Fringe Size: {fsize}")
            print(f"Goal reached at depth {level} at a cost of {cost}.")
            print("Steps:")
            for step in move[1:]:
                print(step)
            writegoalonfile(node, cost, level, pathway[-1], move[-1])
            break

        # Skip if the node is already in the closed list
        if any((node == x).all() for x in closed):
            continue

        # Generate successors and update fringe
        successors = expand(node, cost, level, method, pathway, move)
        generated += successors
        closed.append(node)
        if Flag == "true":
            writeonfile(node, cost, level, pathway[-1], move[-1], successors)
        expanded += 1

        # Update max fringe size
        fsize = max(fsize, len(fringe["states"]))

if method == "a*":
    while fringe["states"]:
        # Find the node with the lowest f(n) value
        lowest_fvalue_index = fringe["fnvalue"].index(min(fringe["fnvalue"]))
        
        # Pop the node with the lowest f(n) value
        node, cost, level, pathway, move, heuristic, fnvalue = (
            fringe["states"].pop(lowest_fvalue_index),
            fringe["cost"].pop(lowest_fvalue_index),
            fringe["level"].pop(lowest_fvalue_index),
            fringe["path"].pop(lowest_fvalue_index),
            fringe["action"].pop(lowest_fvalue_index),
            fringe["heuristic"].pop(lowest_fvalue_index),
            fringe["fnvalue"].pop(lowest_fvalue_index)
        )
        popped += 1

        # Check if the goal is reached
        if (node == goal).all():
            print(f"Nodes Popped: {popped}")
            print(f"Nodes Expanded: {expanded}")
            print(f"Nodes Generated: {generated}")
            print(f"Max Fringe Size: {fsize}")
            print(f"Goal reached at depth {level} at a cost of {cost}.")
            print("Steps:")
            for step in move[1:]:
                print(step)
            writegoalonfile(node, cost, level, pathway[-1], move[-1], fnvalue)
            break

        # Skip if the node is already in the closed list
        if any((node == x).all() for x in closed):
            continue

        # Generate successors and update fringe
        successors = expand(node, cost, level, method, pathway, move)
        generated += successors
        closed.append(node)
        if Flag == "true":
            writeonfile(node, cost, level, pathway[-1], move[-1], fnvalue, successors)
        expanded += 1

        # Update max fringe size
        fsize = max(fsize, len(fringe["states"]))


if method == 'dls':
    limit = int(input("Enter the depth limit: "))  # Get depth limit from user
    max_iterations = 1000  # Prevent infinite loops
    iteration = 0
    while fringe["states"] and iteration < max_iterations:
        iteration += 1
        print("Processing node:")
        print(node)
        node, cost, level, pathway, move = (
            fringe["states"].pop(),
            fringe["cost"].pop(),
            fringe["level"].pop(),
            fringe["path"].pop(),
            fringe["action"].pop()
        )
        popped += 1

        if (node == goal).all():
            print("Goal reached!")
            print(f"Nodes Popped: {popped}")
            print(f"Nodes Expanded: {expanded}")
            print(f"Nodes Generated: {generated}")
            print(f"Max Fringe Size: {fsize}")
            print(f"Goal reached at depth {level} at a cost of {cost}.")
            print("Steps:")
            for step in move[1:]:
                print(step)
            writegoalonfile(node, cost, level, pathway[-1], move[-1])
            break

        if level >= limit:
            print("Depth limit reached. Skipping node.")
            continue

        print("Generating successors...")
        successors = expand(node, cost, level, method, pathway, move)
        generated += successors
        if Flag == "true":
            print("Writing to dump.txt...")
            writeonfile(node, cost, level, pathway[-1], move[-1], successors)
        expanded += 1

        fsize = max(fsize, len(fringe["states"]))
        print("Updated Fringe Size:", fsize)

if method == 'ids':
    limit = 0

    while True:
        # Reset fringe for each depth limit iteration
        fringe["states"] = [start]
        fringe["cost"] = [0]
        fringe["level"] = [0]
        fringe["path"] = [[None]]
        fringe["action"] = [[None]]

        goal_found = False  # Track if the goal is found

        while fringe["states"]:
            node, cost, level, pathway, move = (
                fringe["states"].pop(),
                fringe["cost"].pop(),
                fringe["level"].pop(),
                fringe["path"].pop(),
                fringe["action"].pop()
            )
            popped += 1

            if (node == goal).all():
                print(f"Nodes Popped: {popped}")
                print(f"Nodes Expanded: {expanded}")
                print(f"Nodes Generated: {generated}")
                print(f"Max Fringe Size: {fsize}")
                print(f"Goal reached at depth {level} at a cost of {cost}.")
                print("Steps:")
                for step in move[1:]:
                    print(step)
                writegoalonfile(node, cost, level, pathway[-1], move[-1])
                goal_found = True  # Mark goal as found
                break  # Stop searching in the current iteration

            if level < limit:
                successors = expand(node, cost, level, method, pathway, move)
                
                if isinstance(successors, list):  # Ensure it's a list of successor states
                    generated += len(successors)
                    for succ in successors:
                        fringe["states"].append(succ["state"])
                        fringe["cost"].append(succ["cost"])
                        fringe["level"].append(succ["level"])
                        fringe["path"].append(succ["path"])
                        fringe["action"].append(succ["action"])
                else:
                    generated += successors  # If it returns an integer count

                if Flag == "true":
                    writeonfile(node, cost, level, pathway[-1], move[-1], successors)

                expanded += 1
                fsize = max(fsize, len(fringe["states"]))

        if goal_found:
            break  # Exit the entire IDS loop

        limit += 1  # Increase depth limit for the next iteration
