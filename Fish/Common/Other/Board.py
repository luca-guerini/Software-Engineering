#!/usr/bin/env python3
from enum import Enum
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from typing import Tuple, List, Dict
import random
from coordinatetransformer import coordinate_transform as marshalposn
import copy
path = "./Other/Images/"
class Color(str,Enum):
    RED = "red"
    WHITE = "white"
    BROWN = "brown"
    BLACK = "black"
    #determines enum equality because
    #my enum implementation using multiple inheritance
    #short circuits ordinary enum equality.
    #this overrides the method... to restore previous functionality.
    #Because Python is a weird language.
    def __eq__(self, othercolor):
        return self.value == othercolor.value
    #Like __eq__... overrides hash enumeration...
    #to restore hash enumeration. :/
    def __hash__(self):
        return hash(self.value)
#Basic Exception class for handling the
#incidence of a Player cheating.
class PlayerCheatException(Exception):
    def __init__(self,message):
        self.message = message
class Penguin:
    # __init__: (Tuple[int, int, int], str) -> None
    # Purpose: Initialize a Penguin object with color (R,G,B) and ownership as a string.
    def __init__(self, colour: Color):
        self.colour = colour
    def __eq__(self,other):
        return self.colour.value == other.colour.value
    def COLOR(self):
        return self.colour
class Tile:
    # __init__: (int, int, int) -> None
    # Purpose: Initialize a Tile object with x and y coordinates and fish count.
    def __init__(self, x: int, y: int, fish: int=0,penguin: Penguin=None):
        self.x = x
        self.y = y
        self.fish = fish
        self.penguin = penguin
        if fish > 0:
            self.standing = True
        else:
            self.standing = False
    #VALUE: -> natnum
    #Purpose: Returns the number of fish on the Tile
    def VALUE(self)->int:
        return self.fish
    #X: -> natnum
    #Purpose: Returns the X coordinate of the Tile
    def X(self)->int:
        return self.x
    #Y: -> natnum
    #Purpose; Returns th Y coordinate of the Tile
    def Y(self)->int:
        return self.y
    #positions: -> (int,int)
    #purpose: returns x and y together.
    def position(self)->Tuple[int,int]:
        return (self.x,self.y)
    #dunder method determining equality
    def __eq__(self,other):
        return (self.x == other.x) and (self.y==other.y) and (self.fish==other.fish) and (self.resident()==other.resident())
    #dunder method determining lt relationships
    def __lt__(self,other):
        if (self.y >=other.y) and (self.x >= other.x):
            return False
        elif (self.y==other.y) and (self.x< other.x):
            return True
        else:
            return True
    # add_penguin: (Penguin) -> None
    # Purpose: Add a penguin to the tile.
    def add_penguin(self, penguin: Penguin):
        if self.vacant(): #TODO: add penguin only if tile is standing HERE
            self.penguin = penguin
        else:
            raise PlayerCheatException(penguin.COLOR())
    # remove_penguin: () -> None
    # Purpose: Remove a penguin from the tile, then sink it.
    def remove_penguin(self):
        self.penguin = None
        self.set_standing(False)
    # collect_fish: () -> int
    # Purpose: Collect fish from the tile if it's standing and has fish.
    # Effect: Reduces the fish count on the tile by 1.
    def collect_fish(self) -> int:
        num = copy.deepcopy(self.fish)
        self.fish = 0
        return num
    #resident: -> Penguin or None
    #Purpose: Returns the resident of the tile (if there is one)
    def resident(self):
        return self.penguin
    # is_occupied: () -> bool
    # Purpose: Check if the tile is occupied by a penguin.
    def is_occupied(self) -> bool:
        return isinstance(self.penguin,Penguin) or (not self.standing)
    #vacant: -> bool
    #Purpose: is_occupied, but not.
    def vacant(self)->bool:
        return self.standing and (not isinstance(self.penguin,Penguin))
    # set_standing: (bool) -> None
    # Purpose: Set the standing state of the tile.
    def set_standing(self, standing: bool):
        self.standing = standing
    #is_standing: -> bool
    #Purpose: returns whether or not the tile is standing
    def is_standing(self) -> bool:
        return self.standing
    
    # render: -> pygame.Surface
    # Purpose: Render the tile as a pygame.Surface.
    def render(self,tile_size) -> pygame.Surface:
        if not self.is_standing():
            # If the tile is not standing, return the surface of emptiness.png
            return pygame.image.load(path+"emptiness.png")
        elif self.is_occupied():
            # If the tile is occupied, return the surface based on the penguin color
            penguin_color = self.penguin.COLOR()

            penguin_image = f"{penguin_color}penguin.png"
            return pygame.transform.scale(pygame.image.load(path+f"{penguin_image}"), (tile_size, tile_size))
        else:
            # If the tile is not occupied, return the surface based on the fish count
            fish_count = self.fish
            return pygame.transform.scale(pygame.image.load(path+f"{fish_count}fish.png"), (tile_size, tile_size))
    #marshal: -> int
    #Purpose: Marshals tile.
    #Seems basic, but that is because one cannot easily marshal a value
    #into its appropraite matrix index.
    def marshal(self):
        return self.fish

class Board:
    # __init__: (int, int, int) -> None
    # Purpose: Initialize a Board object with size, tile size, tiles, and penguins.
    def __init__(self, tile_list,tile_size=40):
        self.tile_size = tile_size
        self.tiles = dict()
        self.penguins = []
        self.size= len(tile_list)
        self.size_x = 1
        self.size_y = 1
        for tile in tile_list:
            self.tiles[tile.position()] = tile
            if tile.position()[0] >= self.size_x:
                self.size_x = tile.position()[0]+1
            if tile.position()[1] >= self.size_y:
                self.size_y = tile.position()[1]+1
    #Purpose: Returns a String representation of the Board.
    def to_string(self):
        r = "\n"
        for x,y in self.positions():
            r+=f"({x},{y}) F:{self.tiles[(x,y)].VALUE()}"
        return r
    #dimensions: -> Tuple[nat,nat]
    #Purpose: Returns the dimensions (len(x),len(y)) of the board as a Tuple
    def dimensions(self):
        return (self.size_x,self.size_y)
    #Purpose: Determines board equality.
    def __eq__(self,other):
        return sorted(self.tiles) == sorted(other.tiles)
    #Purpose: Dunder returning number of tiles in the board.
    def __len__(self):
        return self.size
    #positions: -> List[Tuple[nat,nat]]
    #Purpose: Returns the Positions located on the Board.
    def positions(self)->List[Tuple[int,int]]:
        return self.tiles.keys()
    def getTiles(self):
        return self.tiles.values()
    # get_tile: (int, int) -> Tile or None
    # Purpose: Get the tile at the specified coordinates (x, y)
    def get_tile(self, x:int, y:int) -> Tile:
        try:
            return self.tiles[(x,y)]
        except KeyError:
            return None
    #collect_fish: (int, int) -> int
    #Purpose: If there are fish on a given tile, collects the fish.
    def collect_fish(self,x: int, y: int):
        return self.tiles[(x,y)].collect_fish()
    # add_penguin: (Penguin, int, int) -> None
    # Purpose: Add a penguin to the specified tile (x, y).
    def add_penguin(self, penguin: Penguin, x: int, y: int):
        try:
            self.tiles[(x,y)].add_penguin(penguin)
            self.penguins.append(penguin)
        except (PlayerCheatException, AttributeError,KeyError):#Rule-breaking moves, invalid tiles, and non-existent tiles.
            raise PlayerCheatException(penguin.COLOR())
    #PENGUINS: -> List[Penguin]
    #Purpose: Returns the list of Penguins.
    def PENGUINS(self):
        return self.penguins
    #load_penguins: List[posn] + Color -> Effect
    #Purpose: This is a method called when a Board is loaded from JSON
    #to add the Penguins to the Board.
    def load_penguins(self,penguinslist: List,col: Color):
        for location in penguinslist:
            try:
                self.tiles[(location)].set_standing(True)
                self.add_penguin(Penguin(col),*location)
            except PlayerCheatException as e:
                raise e
    #remove_penguin: int int -> Effect!
    #Purpose: Removes a penguin from the tile coordinate, and sets the tile's
    #standing status to not standing.
    def remove_penguin(self, x: int, y: int):
        self.tiles[(x,y)].remove_penguin()
    # remove_tile: (int, int) -> None
    # Purpose: Remove a tile from the board at the specified coordinates (x, y).
    def remove_tile(self, x: int, y: int):
        tile = self.get_tile(x, y) #TODO: Add error to un-standing a fallen tile.
        if tile:
            self.tiles[(x,y)].set_standing(False)
    #get_penguin: int int -> Penguin or None
    #Purpoe: Returns a penguin if there is one on the tile, otherwise none.
    def get_penguin(self, x: int, y: int):
        return self.get_tile(x,y).penguin
    # render: () -> pygame.Surface
    # Purpose: Render the entire board as a pygame.Surface.
    def render(self) -> pygame.Surface:
        #dimensions of screen:
        dimensions = (1280,1280)
        # Create a surface to draw the board
        board_surface = pygame.Surface(dimensions)

        # Set the background of the board surface to background.png
        background_image = pygame.image.load(path+"background.png")
        background_image = pygame.transform.scale(background_image, (1280,1280))
        board_surface.blit(background_image, (0, 0))

        # Loop through each tile and blit its surface onto the board surface
        for tile in self.getTiles():
            tile_surface = tile.render(self.tile_size)
            tile_coordinates = self.get_tile_coordinates(tile)
            board_surface.blit(tile_surface, tile_coordinates)

        # Return the rendered board surface
        return board_surface

    # get_tile_coordinates: (Tile) -> Tuple[int, int]
    # Purpose: Get the pixel coordinates for a given tile.
    def get_tile_coordinates(self, tile: Tile) -> Tuple[int, int]:
        x, y = tile.X(),tile.Y()
        offset_x = self.tile_size * 3 / 6 if x % 2 == 1 else 0
        return int(x * self.tile_size*0.75), int(y * self.tile_size+offset_x)
    #Reachable: Tile -> List[Tiles]
    #Purpose: Determines the tiles reachable via straight lines.
    #A tile is unreachable when it's not in a straight line, or obstructed
    #by a non-standing tile.
    #Requirement: Tile is in the Board.
    def reachable(self, col: int or Tile, row:int,tile_strategy=(lambda x,y: (x+10,y)))->List[Tuple[int,int]]:
        x,y = tile_strategy(col.X(),col.Y()) if (isinstance(col,Tile)) else tile_strategy(col,row)
        result = []
        def tile_exists_and_not_occupied(x,y):
            tile = self.get_tile(x,y)
            return isinstance(tile,Tile) and (0<= tile.X() < self.dimensions()[0]) and (0<= tile.Y() < self.dimensions()[1]) and (not tile.is_occupied())
        while tile_exists_and_not_occupied(x,y):
            result.append((x,y))
            x,y = tile_strategy(x,y)
        return result
    def check_south(self,col: int or Tile, row: int=-1):
        def strategy(x,y):
            return (x,y+1)
        return self.reachable(col,row,tile_strategy=strategy)
    def check_north(self,col: int or Tile, row: int=-1):
        def strategy(x,y):
            return (x,y-1)
        return self.reachable(col,row,tile_strategy=strategy)
    def check_southeast(self, col: int or Tile, row: int=-1):
        def strategy(x,y):
            return (x+1,y) if x%2==0 else (x+1,y+1)
        return self.reachable(col,row,tile_strategy=strategy)
    def check_northeast(self,col: int or Tile, row: int=-1):
        def strategy(x,y):
            return (x+1,y) if x%2==1 else (x+1,y-1)
        return self.reachable(col,row,tile_strategy=strategy)
    def check_southwest(self,col: int or Tile, row: int=-1):
        def strategy(x,y):
            return (x-1,y+1) if x%2==1 else (x-1,y)
        return self.reachable(col,row,tile_strategy=strategy)
    def check_northwest(self,col: int or Tile, row: int=-1):
        def strategy(x,y):
            return (x-1,y) if x%2==1 else (x-1,y-1)
        return self.reachable(col,row,tile_strategy=strategy)
    #adjacent: itn int -> bool
    #Purpose: returns true if the give (x,y) has a standing neighbor that is unoccupied
    #Implemented despite the existence of reachable(x,y) because it's a fast way to
    #investigate whether or not a board will have a valid successor state.
    def has_adjacent(self,x:int,y:int):
        def evens():
            return (self.get_tile(x-1,y-1).vacant()) or (self.get_tile(x-1,y).vacant()) or (self.get_tile(x+1,y-1).vacant()) or (self.get_tile(x+1,y).vacant())
        def northsouth():
            return (self.get_tile(x,y+1).vacant()) or (self.get_tile(x,y-1).vacant())
        def odds():
            return (self.get_tile(x-1,y).vacant()) or (self.get_tile(x-1,y+1).vacant()) or (self.get_tile(x+1,y).vacant()) or (self.get_tile(x+1,y+1).vacant())
        try:
            if x%2==0:
                return (evens() or northsouth())
            else:
                return (odds() or northsouth())
        except AttributeError:
            return False#The context in which this method is used means I don't care if I call the method
            #On an input that causes an attribute error. This method should only be used for its utility as a shortcut
            #in time and computational cost to self.reachable(x,y)
    #reachable_tiles: nat nat -> List[Tuple[int,int]]
    #Purpose: return the indexes reachable from the given natnum coordinates
    #as a list of tuples.
    def reachable_indexes(self,x:int,y:int):
        return (self.check_north(x,y)+self.check_northeast(x,y)+self.check_southeast(x,y)+self.check_south(x,y)+self.check_southwest(x,y)+self.check_northwest(x,y))
    #reachable_tiles: int int -> List[Tile]
    #Purpose: determines tiles reachable from the provided x,y indices if any.
    def reachable_tiles(self,x: int, y: int)-> List[Tile]:
        real_tiles = []
        for posn in self.reachable_indexes(x,y):
            real_tiles.append(self.get_tile(posn[0],posn[1]))
        return real_tiles
    #marshal: -> List[List[int]]
    #Purpose: marshals the board into JSON.
    def marshal(self):
        rows,cols = marshalposn(*self.dimensions())
        rows = len(self)//cols
        return [([self.tiles[posn].marshal() for posn in self.positions()])[x*cols:((1+x)*cols)] for x in range(rows)]
#demarshal_board: List[List[nat]] -> Board
#Purpose: demarshals a board.
def demarshal_board(boardlist:List):
    tile_list = []
    x = 0
    y = 0
    for row in boardlist:
        for col in row:
            r, c = marshalposn(x,y)
            tile_list.append(Tile(r,c,fish=col))
            y+=1
        x+=1
        y=0
    return Board(tile_list)
    #return Board(tile_list=[Tile(*coordinate_transform(row,col),boardlist[row][col]) for row in range(len(boardlist)) for col in range(len(boardlist[row]))])
#random_board: int int int bool -> Board
#Purpose: Generates a Board object with a random number of fish.
#rows indicates the number of rows
#cols indicates the number of cols
#min_ones indicates the number of 1 fish tiles. By default, the value is -1 which will indicate
#that all tiles should have at least 1 fish.
#holes decides whether or not the board should be generated with holes in it.  
def random_board(rows,cols,min_ones=-1,holes=False):
    min_ones = rows*cols if min_ones<0 else min_ones
    hole_val = 0 if holes else 1
    def gen_tiles(r,c,min):
        lst = []
        tiles = []
        for x in range(r+c):
            lst.append(1) if x<min else lst.append(random.randint(hole_val,5))
        random.shuffle(lst)
        for y in range(r):
            for x in range(c):
                tiles.append(Tile(x,y,fish=lst[x+y]))
        return tiles
    if min_ones == 0:
        return Board(gen_tiles(rows,cols,min_ones))
    elif min_ones < 0:
        raise ValueError
    else:
        return Board(gen_tiles(rows,cols,min_ones))
# Example usage:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 1280))
    board = random_board(6,6,8)
    board.tile_size = 80
    penguin1 = Penguin(colour=Color.RED)
    board.add_penguin(penguin1, 2, 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(board.render(),(0,0))
        pygame.display.flip()

    pygame.quit()