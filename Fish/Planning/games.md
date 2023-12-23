State Data Representation.

Data-wise, a Game State is a Class with the following attributes:
1. A Data Representation of a Board
    1a. The Board has the following attributes
        a. A Dictionary/Hash Table of Tiles whose keys
        relate to their coordinate on the game board.
            (N.B.) Python implements Dictionaries as Hash tables, but this is declared/initialized as a dict(). This is
            to clarify that there is only a semantical difference between a Dictionary and a basic Hash Table in Python.
        b. A Set of penguins in play (Set[Penguin])
        c. A rendering function (Pygame.Surface)
2. A List of Players
    1a. The List of Players is a Dictionary of Players, and I will define the structure a Player of now:
        a. Color: The Color of the Player's penguins (Enum)
        b. Score: The number of points (fish) accrued by the player during the course of the game. (Int)
        c. Places: The places on the board where a player has penguins. (Positions: Tuple[Int,Int])
    2a. As for the Player Dictioanry itself:

In terms of functionality, the State class handles the placement and moving of player penguins,
as well as determining ownership of Penguins on the Board and whether they can be moved by a player.

There is an Exception class called PlayerCheatException that is raised whenever an invalid move is submitted to the
game.