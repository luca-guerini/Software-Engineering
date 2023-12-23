import sys, os
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common/Other'))
from typing import Callable, Tuple
import unittest, random
from coordinatetransformer import coordinate_transform as transform
from hypothesis import given, settings
from hypothesis.strategies import integers, composite, SearchStrategy, tuples
import copy
@composite
def rand_coord(draw: Callable[[SearchStrategy[int]],int],min_value=0,max_value=65536):
#I don't see a need to test more than 2^16 because I can't think of a game with even that many tiles.
    x = draw(integers(min_value,max_value))
    y = draw(integers(min_value,max_value))
    return (x,y)
#f(f(x)) = f(x)  x ∈ (0,65536)
@given(rand_coord())
@settings(max_examples=1000)#It's weird syntax, but I'm saying to run 100000 tests.
def test_coordinatetransform(tup):
    x,y = tup
    x2,y2 = copy.deepcopy(tup) #Take copies of the tuple values
    x2,y2 = transform(*transform(x2,y2)) #transform the copy twice
    assert x2 == x #Assert equality
    assert y2 == y #Assert equality