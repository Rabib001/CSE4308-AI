import argparse
import math

def parse_args():
    parser = argparse.ArgumentParser(description="Red-Blue Nim Game")
    parser.add_argument("num_red", type=int, help="Number of red marbles")
    parser.add_argument("num_blue", type=int, help="Number of blue marbles")
    parser.add_argument("version", nargs="?", default="standard", choices=["standard","misere"] help="Game version (default: standard)")    #optional in command line
    parser.add_argument("first_player", nargs="?", default="computer", choices=["computer","human"] help="First player (default: computer)")    #optional in command line
    parser.add_argument("depth", nargs="?", type=int, help="Depth limit for the search")    #optional in command line(for extra credit)
    return parser.parse_args()

#Check if game reached terminal state
def terminal_test(state):
    return state[0] == 0 or state[1] == 0

#calculate score
def score(state, version):
    red, blue = state
    scr = 2*red + 3*blue
    if version == "standard":
        return scr
    else:
        return -scr
    
#generate valid moves
def successors(state):
    moves = []
    if state[0] > 0:
        moves.append(("red", 1))
        if state[0] > 1:
            moves.append(("red", 2))
    if state[1] > 0:
        moves.append(("blue", 1))
        if state[1] > 1:
            moves.append(("blue", 2))
    return moves

#take current game state and return a new state
def move_marble(state, mv):
    pile, count = mv
    if pile == "red":
        return (state[0]-count, state[1])
    else:
        return (state[0], state[1]-count)
    
def max_val(state, alpha, beta, depth, version):
    if terminal_test(state) or depth == 0:
        return score(state, version)
    v = -math.inf
    for move in successors(state):
        new_state = move_marble(state, move)
        v = max(v, min_val(new_state, alpha, beta, depth - 1, version))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_val(state, alpha, beta, depth, version):
    if terminal_test(state) or depth == 0:
        return score(state, version)
    v = math.inf
    for move in successors(state):
        new_state = move_marble(state, move)
        v = min(v, max_val(new_state, alpha, beta, depth - 1, version))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def alpha_beta_decision(state, depth, version):
    best_move = None
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf
    for move in successors(state):
        new_state = move_marble(state, move)
        value = min_val(new_state, alpha, beta, depth - 1, version)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)
    return best_move

def computer_move(state, version, depth=None):
    if depth in None:
        depth = math.inf
    return alpha_beta_decision(state, version, depth)

def human_move(state):
    while True:
        pile = input("Choose a pile (red/blue): ").strip().lower()
        if pile not in ["red", "blue"]:
            print("Invalid pile. Please choose red or blue.")
            continue
        count = input(f"Enter number of marbles to remove from {pile} pile (1 or 2): ").strip()
        if count not in ["1", "2"]:
            print("Invalid number of marbles. Please choose 1 or 2.")
            continue
        count = int(count)
        if (pile == "red" and state[0] < count) or (pile == "blue" and state[1] < count):
            print("Not enough marbles in the pile. Please choose a smaller number.")
            continue
        return (pile, count)