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
def terminal_state(state):
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
def move(state, mv):
    pile, count = mv
    if pile == "red":
        return (state[0]-count, state[1])
    else:
        return (state[0], state[1]-count)
    
