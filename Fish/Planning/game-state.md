Data Implementations:

Penguin
Penguin is a stand-in for the game pieces used by the players.
It has two properties, color and ownership.
The color property is a tuple that represents teh RGB value (in gameplay, this will always be Red, White, Brown, or Black.

Tile
A tile object represents an individual game tile.
It has an x and a y coordinate, as well as
Fish: which represents the number of fish on the title
Penguin: which represents whether or not a penguin is on the tile.
standing: A boolean that determines whether or not the tile is still traversible.
Logic-wise, the tile should never need to be considered for anything if it is not standing.

Board
Board is an object that contains a list of Tiles.
Game state changes based on player actions, which cause changes on the Board.
Players might move their penguins, collect fish, etc.

