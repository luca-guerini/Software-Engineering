#!/usr/bin/env python3
def coordinate_transform(x, y):
    return (y*2,x//2) if x%2==0 else ((y*2+1),(x-1)//2)