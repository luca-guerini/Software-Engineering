#!/usr/bin/env python3
import copy
import sys, os
from typing import Callable, Tuple, List
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common'))
sys.path.append(os.path.expanduser('~/guerinlu/Fish/Common/Other'))
from Board import Board, Tile, Color
from state import State, Player
import unittest, random
from hypothesis import example, given, settings, HealthCheck, assume
from hypothesis.strategies import integers, composite, sampled_from, lists
###GameTree related Class and Functions to Test.###
from game_tree import GameTree as GT
from game_tree import kickPlayer as KICK
from game_tree import find_winners as WINNERS
@composite
def state_strategy(draw):
    player_colors = [Color.RED, Color.WHITE, Color.BROWN, Color.BLACK]
    num_players = draw(integers(min_value=2, max_value=4))
    random.shuffle(player_colors)

    players = []
    tiles = []
    # Generate tiles
    for x in range(10):
        for y in range(10):
            fish = draw(integers(min_value=0, max_value=5))
            tile = Tile(x=x, y=y, fish=fish,penguin=None)
            tiles.append(tile)

    board = Board(tile_list=tiles)
    all_positions = list(board.tiles.keys())
    # Generate players and places
    for color in player_colors[:num_players]:
        score = draw(integers())
        
        # Ensure player places do not share values
        places = draw(
            lists(
                sampled_from(all_positions),
                min_size=6 - num_players,
                max_size=6 - num_players,
                unique=True
            )
        )
        # Update the pool of available positions
        all_positions = list(set(all_positions) - set(places))
        #add player
        players.append(Player(colour=color, score=score, places=places))
    return State(players=players, board=board)

@composite
def valid_movable_game_tree_strategy(draw):
    statum = state_strategy(draw)
    tile = 
@given(state_strategy())
@settings(suppress_health_check=list(HealthCheck))
def test_marshall_demarshal(state: State):
    statecopy = copy.deepcopy(state)
    marshaled = demarshal_state(state.marshal())
    assert statecopy == marshaled