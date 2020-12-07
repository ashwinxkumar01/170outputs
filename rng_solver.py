import networkx as nx
from parse import read_input_file, write_output_file
from utils import *
import sys
from os.path import basename, normpath
import glob
import numpy as np
import random

def solve(G, s, n):
    # check cases with 1 breakoutroom or n breakout rooms
    bestD = {}
    bestHap = 0
    bestK = 0
    for k in np.arange(1, n+1):
        maxStressPerRoom = s/k
        repetition = 1000
        for i in np.arange(repetition):
            D = {}
            people = list(np.arange(n))
            random.shuffle(people)
            #fill up k breakout rooms
            counter = k
            for person in people: 
                if counter != 0: # put one random person in each breakout room
                    D[counter - 1] = [person];
                    counter = counter - 1;
                else:
                    # compare with rooms
                    possibleRooms = {}
                    bestRatio = 0
                    for room in D:
                        tmp = D[room] + [person]
                        personStress = calculate_stress_for_room(tmp, G)
                        personHap = calculate_happiness_for_room(tmp, G)
                        if personStress == 0:
                            ratio = personHap 
                        else:
                            ratio = personHap/personStress
                        if personStress <= maxStressPerRoom:
                            possibleRooms[room] = ratio
                    if len(possibleRooms) == 0: 
                        break
                    else:
                        possibleRooms = {k: v for k, v in sorted(possibleRooms.items(), key=lambda item: item[1], reverse = True)}
                        roomsList = list(possibleRooms.keys())
                        if random.uniform(0,1) <= 0.5:
                            random.shuffle(roomsList)
                        selectedRoom = roomsList[0]                        
                        D[selectedRoom] = D[selectedRoom] + [person]
            D = convert_dictionary(D)
            if is_valid_solution(D, G, s, k) and len(D) == n and calculate_happiness(D, G) >= bestHap:
                bestHap = calculate_happiness(D, G)
                bestD = D
                bestK = k
    print("Dictionary is ", bestD)
    print("Best Happiness is", calculate_happiness(bestD, G))
    print("k is ", k)
    return bestD, bestK

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    n = 20
    for i in np.arange(165, 180):
        if i+1 != 219 and i+1 != 225:
            G, s = read_input_file('./inputs/medium-{num}.in'.format(num = i + 1))
            D, k = solve(G,s,n)
            write_output_file(D, 'outputs/medium-{num}.out'.format(num = i + 1))

# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
