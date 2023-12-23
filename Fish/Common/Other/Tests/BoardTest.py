#!/usr/bin/env python3
import sys, os
from typing import Callable, Tuple, List
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common/Other'))
from Board import *
import random
from hypothesis import example, given, settings, assume
from hypothesis.strategies import integers, composite, SearchStrategy, tuples

#TESTS FOR GENERATING RANDOM BOARDS WITH NO HOLES
@composite
def rand_board(draw: Callable[[SearchStrategy[int]],int],min_value: int = 1, max_value: int = 100):
    x_random = draw(integers(min_value,max_value))
    y_random = draw(integers(min_value,max_value))
    return random_board(x_random,y_random,min_value,holes=False)

@given(rand_board())
def test_board_length(board: Board):
    assert board.dimensions()[0]*board.dimensions()[1] == len(board)

@given(rand_board())
def test_get_tile(board: Board):
    x = random.randint(0,board.size_x-1)
    y = random.randint(0,board.size_y-1)
    assert board.get_tile(x,y).position() == (x,y)
    assert board.get_tile(-1,-1) == None

@given(rand_board())
def test_reachable(board: Board):
    assume(len(board)>=1)
    x = random.randint(0,board.size_x-1)
    y = random.randint(0,board.size_y-1)
    if len(board) > 1:
        assert len(board.reachable(x,y)) >= 0 #should always be true for a hole-less random board.
    else:
        assert len(board.reachable(x,y)) == 0
@given(rand_board())
def test_penguin_stuff(board: Board):
    #add_penguin
    x = random.randint(0,board.size_x-1)
    y = random.randint(0,board.size_y-1)
    a_penguin = Penguin(Color.RED)
    assert board.get_penguin(x,y) == None
    assert board.get_tile(x,y).is_standing()
    assert board.get_tile(x,y).is_occupied() == False
    board.add_penguin(a_penguin,x,y)
    assert board.get_penguin(x,y) == a_penguin
    assert board.get_tile(x,y).is_standing() == True
    assert board.get_tile(x,y).is_occupied() == True
    board.remove_penguin(x,y)
    assert board.get_penguin(x,y) == None
    assert board.get_tile(x,y).is_standing() == False
    assert board.get_tile(x,y).is_occupied() == True

    
@given(rand_board())
def test_reachable_input_variations(board: Board):
    a = random.randint(0,board.size_x-1)
    b = random.randint(0,board.size_y-1)
    mint = board.get_tile(a,b)
    assert board.check_south(mint) == board.check_south(a,b)
    assert board.check_north(mint) == board.check_north(a,b)
    assert board.check_southeast(mint) == board.check_southeast(a,b)
    assert board.check_southwest(mint) == board.check_southwest(a,b)
    assert board.check_northeast(mint) == board.check_northeast(a,b)
    assert board.check_northwest(mint) == board.check_northwest(a,b)

@given(rand_board())
def test_reachable_invariants(board: Board):
    x = random.randint(0,board.size_x-1)
    y = random.randint(0,board.size_y-1)
    def reachable_assertion(tiles: List[Tuple[int,int]], strategy):
        def find(posn: Tuple[int,int],numcalls: int):
            while numcalls > 0:
                posn = strategy(posn[0],posn[1])
                numcalls-=1
            return posn
        #even_tiles = filter(tiles,lambda x: x%2==0)
        #odd_tiles = filter(tiles,lambda x: x%2==1)
        for x in range(len(tiles)-1):
            assert tiles[x+1] == find(tiles[x],1) #Asserting that each tile in a list of parallel tiles is a particular transformation of the previous tile.
    south = lambda x,y: (x,y+1)
    north = lambda x,y: (x,y-1)
    southeast = lambda x,y: (x+1,y) if x%2==0 else (x+1,y+1)
    southwest = lambda x,y: (x-1,y+1) if x%2==1 else (x-1,y)
    northeast = lambda x,y: (x+1,y) if x%2==1 else (x+1,y-1)
    northwest = lambda x,y: (x-1,y) if x%2==1 else (x-1,y-1)
    reachable_assertion(board.check_south(x,y),south)
    reachable_assertion(board.check_north(x,y),north)
    reachable_assertion(board.check_southeast(x,y),southeast)
    reachable_assertion(board.check_southwest(x,y),southwest)
    reachable_assertion(board.check_northeast(x,y),northeast)
    reachable_assertion(board.check_northwest(x,y),northwest)

