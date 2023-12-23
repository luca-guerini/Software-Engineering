API for Fish

Fish is a game played over a hex tile grid with 2-4 (P) players controlling (6-P) penguins each.
Additionally, players are assigned a Color at the beginning of a game as Red, White, Brown, or Black.

As such, a game state can be described as the following:
A hex tile grid, represented by an RxC matrix in column major, where each integer
represents the number of fish on a tile.

For example:
[[1,2,3],[4,5,6],[7,8,9],[10,11,13]]

This represents a board with 1 fish on the top-left-most tile, and 13 fish on the bottom-right-most tile,
and we can visualize the arrangement of tiles like this:
[[1  2  3]
 [4  5  6]
 [7  8  9]
 [10 11 12]]

where each tile is connected to its vertical or diagonal neighbors.

Additionally, the data keeps track of the players in the game according to the relevant information:
Color: String
Score: Natural Number
Penguin Placements (Natural Number, Natural Number)

A player can thusly be represented as a Python Dictionary, and a JSON object:
{"color": <"red","white","brown", or "black">,
"score": number
"places":(x,y)}

Furthermore, a game is constituted of a list of players taking turns in the order they are organized in the list of players.

[Player1,Player2,Player3,Player4] would move in order from left to right. Thus, we can say that
when Player1 takes her turn, the list should reflect that and be ordered as the following:
[Player2,Player3,Player4,Player1].

Given that, a particular state of the game can be represented as a State,
which is a JSON object of the following:
{"players":List[Players], "board": Board}


