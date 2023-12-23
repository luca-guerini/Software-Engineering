#!/usr/bin/env python3
from enum import Enum
from os import statvfs_result
from typing import Dict, List, Tuple
import Board
from Board import Color, Penguin, Board, Tile, PlayerCheatException
from Board import demarshal_board as deboard
import random
import pygame
from coordinatetransformer import coordinate_transform as marshalposn

class Phase(Enum):
    JOINPHASE = 0#Only for online multiplayer. Not yet implemented.
    PLACEMENT = 1
    PLAY = 2
    VICTORY = 3
#Design and implement a game state data representation.
#A Game state has:
#The state of the board
#The current placements of the penguins
#Knowledge about the players
#and the order in which they play.
class Player:
    def __init__(self, colour: Color=Color.RED, score: int=0, places: List[Tuple[int,int]]=[]):
        self.colour = Color(colour)
        self.score = score
        self.places = places
    #Purpose: Dunder method for determining player equality.
    def __eq__(self,other):
        return ((self.colour == other.colour) and (self.score == other.score) and (self.places == other.places))
    #SETPLACES: List[Posn] -> Effect!
    #Purpose: sets the list of positions.
    def SETPLACES(self,newplaces: List[Tuple[int,int]]):
        self.places = newplaces
    #COLOR: -> Color(Enum)
    #Purpose: Returns player Color
    def COLOR(self)->Color:
        return self.colour
    #COLORSTRING: -> str
    #Purpose: Returns the str associated with a color
    def COLORSTRING(self)->str:
        return self.COLOR().value
    #SCORE: -> int
    #Purpose: Returns an int of the player's score
    def SCORE(self)->int:
        return self.score
    #ADDSCORE: -> Effect!
    #Purpose: adds the inputted number to the player's score
    def ADDSCORE(self,number:int):
        self.score+=number
    #PLACES: -> List[Tuple[Int,Int]]
    #Purpose: Returns the set of places the player has penguins on.
    def PLACES(self)->List[Tuple[int,int]]:
        return self.places
    #ADDPLACE: Effect!
    #Purpose: adds a Place to the List of Places
    def ADDPLACE(self,x:int,y:int):
        self.places.insert(0,(x,y))
    #REMOVEPLACE: Effect!
    #Purpose: removes a place to the List of places
    def REMOVEPLACE(self,x:int,y:int):
        self.places.remove((x,y))
    #CHANGEPLACE: Effect!
    #Purpose: Combines the effects of ADDPLACE and REMOVEPLACE
    def CHANGEPLACE(self,start_x:int,start_y:int,end_x:int,end_y:int):
        self.ADDPLACE(end_x,end_y)
        self.REMOVEPLACE(start_x,start_y)
    #owns: -> bool
    #Purpose: Decides if a player owns a penguin by checking both of their colors.
    def owns(self, penguin: Penguin):
        return self.colour == penguin
    #controls ->: bool
    #Purpose: Decides if a player controls a tile (a player has a penguin on it)
    def controls(self,tile: Tile):
        return isinstance(tile.resident(),Penguin) and self.owns(tile.resident())
    #marshal: -> dict
    #Purpose: marshals the player into a dictionary
    def marshal(self)->dict:
        return {"color": self.COLOR(),"score":self.SCORE(),"places":[marshalposn(*posn) for posn in self.PLACES()]}
    #can_play: -> bool
    #Purpose: Determines whether or not the player has valid moves on any of their penguins,
    #or if they have fewer than the correct number of penguins (and thus can place penguins)
    def can_play(self,board)->bool:
        for penguin in self.PLACES():
            if board.has_adjacent(*penguin):
                return True
        return False
    #Purpose: This is a duner method for less-than,
    #It's written for the purpose not of evaluating
    #players as precedent to one another for any reason
    #other than equality evaluation for game state
    #validation.
    def __lt__(self,other):
        def valueof(player: Player):
            if player.COLOR() == Color.RED:
                return 0
            elif player.COLOR() == Color.WHITE:
                return 1
            elif player.COLOR() == Color.BROWN:
                return 2
            elif player.COLOR() == Color.BLACK:
                return 3
        return (valueof(self) < valueof(other))
class State:
    def __init__(self, board: Board, players: List[Player]=[]):
        self.board = board # Handles state of Board and placements of penguins
        self.players = {} #Players is a Dictioanry of [Color] -> [Player]
        self.numplayers = len(players)
        self.current_player = players[0] #The current player whose turn it is.
        self.turn_order = []
        ###################CONSTRUCTING BOARD##########################
        for player in players:
            self.players[player.COLOR()]=player #The code in this loop maps the dictionary with keys and values.
            board.load_penguins(player.PLACES(),player.COLOR())
            self.turn_order.append(player.COLOR())
        ###################DETERMING PLAY PHASE########################
        self.max_penguins = (6-self.numplayers)*self.numplayers
        if (self.max_penguins > len(self.board.PENGUINS())) and (self.numplayers >= 2):
            self.phase = Phase.PLACEMENT
        elif any(player.can_play(board) for player in players):
            self.phase = Phase.PLAY
        else:
            self.phase = Phase.VICTORY
    #update: -> Effect!
    #updates the board state by revalidating information after a player move has been made.
    #Is basically a function that updates all aspects of the state that are contianed
    #outside of the Board.
    def update(self):
        if (self.current_player.COLOR() == self.turn_order[0]):#If the play order has not yet been updated, then:
            self.turn_order.append(self.turn_order.pop(0)) #rotate the turn order.
        self.current_player = self.players[self.turn_order[0]]#The current player whose turn it is.
        ###################DETERMING PLAY PHASE########################
        if (self.max_penguins > len(self.board.PENGUINS())) and (self.numplayers >= 2):
            self.phase = Phase.PLACEMENT
        elif any(player.can_play(board) for player in players):
            self.phase = Phase.PLAY
        else:
            self.phase = Phase.VICTORY
    #remove_cheater: Color -> Effect!
    #Purpose: Removes a player who offends the rules from the list of palyers. another method handles the removal
    #of their penguins.
    def remove_cheater(self, colour: Color): #This 
        del self.players[colour]
        self.turn_order.remove(colour)
        self.numplayers -= 1
        self.max_penguins-=(6-self.numplayers)*self.numplayers
    def PLAYERS_INORDER(self):
        return [self.players[color] for color in self.turn_order]
    def __eq__(self,other):
        try:
            playersequal = all((self.GETPLAYER(color)==other.GETPLAYER(color)) for color in self.players.keys())
            boardsequal = (self.board == other.board)
            return playersequal and boardsequal
        except KeyError:
            return False
    def PHASE(self):
        return self.phase
    #current_player: -> Player
    #Purpose: returns the player whose turn it currently is.
    def CURRENT_PLAYER(self):#I would have liked to name this 'UTG' in reference to Poker, but not everyone likes playing Poker. :/
        return self.current_player
    #place_penguin: Player + int + int -> Effect!
    #Purpose: Places a penguin on the board if it would be valid to do so.
    #Otherwise, raises an error.
    def place_penguin(self,player: Player,x: int,y: int):
        try:
            #EFFECT!: Penguin is placed.
            self.board.add_penguin(penguin=Penguin(colour=player.COLOR()),x=x,y=y)
            #EFFECT!: player has the position of the added penguin added to his list of penguins
            self.players[player.COLOR()].ADDPLACE(x,y)
            #EFFECT! : player's score is incremented by the number of fish on the tile their penguin is placed on
            self.players[player.COLOR()].ADDSCORE(self.board.collect_fish(x,y))
            #The above line of code demonstrates why imperative programming languages have inscrutable syntax.
        except PlayerCheatException:
            raise PlayerCheatException(player.COLOR())
    #can_move: 
    def can_move(self, player: Player, penguin: Penguin):
        return player.owns(penguin)
    #remove_penguin: int int -> Effect!
    #Purpose: Removes penguin at the given tile.
    #EFFECT! Penguin on given tile is removed.
    def del_penguin(self,x: int, y: int):
        #Effect! penguin is removed on tile.
        self.board.remove_penguin(x,y)
    #move_penguin: Player int int int int -> Effect!
    #Purpose: Moves a penguin.
    #EFFECT! Same effect as place_penguin, except where noted.
    def move_penguin(self,player:Player,start_x:int,start_y:int,end_x:int,end_y:int):
        try:
            #penguin = copy.copy(source.resident()) #make a copy of the source's penguin
            self.place_penguin(player,end_x,end_y) #place the copy on the destination tile.
            self.del_penguin(start_x,start_y) #remove the original penguin
            #EFFECT!: Removes a penguin from the given player's list of places.
            player.REMOVEPLACE(start_x,start_y) #remove the source penguin's Place from their player's Places           
        except (PlayerCheatException, AttributeError):
            raise PlayerCheatException(player.COLOR())
    #BOARD: -> Board
    #Purpose: Returns the game's board
    def BOARD(self)->Board:
        return self.board
    #GETPLAYER: Color -> Player
    #Purpose: Fetches a player by his/her color.
    def GETPLAYER(self,colour: Color):
        return self.players[colour]
    #PLAYERS: -> List[Players]
    #Purpose: Returns the dictioanry of Players as a List
    def PLAYERS(self)->List[Player]:
        return list(self.players.values())
    #PENGUINS(): -> List[Positions]
    #Purpose: Returns the list of positions that penguins are on on the board.
    def PENGUINS(self)->List[Penguin]:
        lst = []
        for x in self.PLAYERS():
            lst = lst + x.PLACES()
        return lst
    #PENGUIN_CAN_MOVE: -> bool
    #Purpose: Determines whether or not any players have a valid move.
    #Designed without using reachable() as a microptimization.
    def PENGUIN_CAN_MOVE(self):
        return any(player.can_play() for player in self.PLAYERS())
    #render: -> Pygame.Surface
    #Purpose: Renders the game state. Identical to what Board does to render the game state.
    def render(self)->pygame.Surface:
        return self.board.render()
    #attributes: -> Tuple[List[Player,Board]]
    #Purpose: Returns the attributes of the current board.
    def attributes(self)->Tuple[List[Player],Board]:
        return ([self.GETPLAYER(colour) for colour in self.turns], self.BOARD())
    #marshal: -> dict
    #Purpose: converts the state object to a dict, which
    #Python's json library can convert into a JSON object when needed.
    def marshal(self):
        return {"players":[player.marshal() for player in self.PLAYERS()],"board": self.board.marshal()}
#buildState: players + board -> State
#Purpose: Builds a State. In truth, likely unecessary.
#I wrote this method /intending/ to add some code to
#basically have a custom initializer As it stands, I
#have not used it.
def buildState(players: List[Player], board: Board):
    return State(board,players)
#demarshal_player: Dict -> Player
#Purpose: Given a dictionary of a player, demarshals it into a Player
def demarshal_player(player: dict)->Player:
    def demarshal_places(places:dict)->List[Tuple[int,int]]:
        return [marshalposn(*posn) for posn in places]
    return Player(player.get("color"),player.get("score"),demarshal_places(player.get("places")))
#demarshal_state: Dict -> State
#Purpose: Given a dictionary, demarshals it into a State.
def demarshal_state(json_dict: dict)->State:
    return State(deboard(json_dict.get("board")),[demarshal_player(player) for player in json_dict.get("players")])