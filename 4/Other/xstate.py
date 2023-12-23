#!/usr/bin/env python3
import sys, os
from typing import *
#Project imports
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common/'))
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common/Other'))
import jutil, json
from state import *
from Board import *
def process(data):
    state = demarshal_state(data)
    the_copy = demarshal_state(data)
    try:
        start_x,start_y = state.CURRENT_PLAYER().PLACES()[0]
        tile_list = state.BOARD().reachable_indexes(start_x,start_y)
        end_x,end_y = tile_list[0] if len(tile_list)>0 else (start_x,start_y)
        #print(f"({start_x,start_y})->({end_x,end_y})")
        state.move_penguin(state.CURRENT_PLAYER(),start_x,start_y,end_x,end_y)
    except PlayerCheatException: #this is going to be how I catch invalid moves, so that's why there's error handling here.
        return "false"
    return "false" if  (state == the_copy) else json.dumps(state.marshal(),indent=None,separators=(',', ':'))
if __name__ == "__main__":
    state_input = jutil.process_json_sequence()[0]
    sys.stdout.write(process(state_input))
    #print("------------------------------------------------")
    #print(demarshal_state(state_input).BOARD().to_string())