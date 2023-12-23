#!/usr/bin/env python3
import os, sys
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common/'))
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common/Other'))
import state, jutil
if __name__ == "__main__":
    def process(data):
        return state.demarshal_state(data)
    def reprocess(data):
        return data.marshal()
    #takes the user input, and converts it into a list to check for --limited
    inputlist = jutil.process_json_sequence()[0]
    inputlist = process(inputlist)
    count = 1
    while(count <= 20):
        lst1 = inputlist.marshal()
        lst2 = process(inputlist.marshal()).marshal()
        if lst1 == lst2:
            print("succeeded!")
        else:
            print("failed!")
        inputlist = process(lst2)
        
        count+=1