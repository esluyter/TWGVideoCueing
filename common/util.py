"""
Utility functions

- clump(list, clump_size)

Author: Eric Sluyter
Last edited: July 2018
"""

def clump(list, clump_size):
    temp = []
    for i in range(0, len(list), clump_size):
        temp.append(list[i:i+clump_size])
    return temp

def make_2d_list(rows, cols, defaultVal=None):
    temp = []
    for i in range(rows):
        temp.append([])
        for j in range(cols):
            temp[i].append(defaultVal)
    return temp
