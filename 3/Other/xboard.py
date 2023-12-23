#!/usr/bin/env python3
import sys, os
from typing import *
from functools import reduce
import math
#Project imports
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common/Other'))
import jutil
from Board import *


def convert(x, y):
    return (y*2,x//2) if x%2==0 else ((y*2+1),(x-1)//2)

def load(data):
    return demarshal_board(data.get("board"))

def num_neighbors(board: Board, x:int,y:int):
    return str(len(board.reachable_indexes(x,y)))
def process(data):
    x,y = convert(*data.get("position"))
    return num_neighbors(load(data),x,y)

def process_print(data):
    def cordstring(posn):
        x,y = posn
        return "("+str(x)+","+str(y)+")"
    x,y = convert(*data.get("position"))
    #x,y = convert(x,y)
    board = load(data)
    reachable = board.reachable_indexes(x,y)
    result = "Examining: (" + str(x)+","+ str(y)+")" +"\n"
    result += "Reachable: ["
    for x in reachable:
        result+= cordstring(x)
    result += "]\n"
    result += "All Positions: " + board.keystring()
    return result +"\n"+ "Number Reachable: " + str(len(reachable))

if __name__ == "__main__":
    json_object_dict = jutil.process_json_sequence()[0]
    sys.stdout.write(process(json_object_dict))
    #print(process_print(json_object_dict))