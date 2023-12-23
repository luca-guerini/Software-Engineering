from typing import Callable, Dict, List
from Other import Player, State, demarshal_state, PlayerCheatException,Phase #Some people take issue with star imports, but since Other only contains my project files, its importing only vital code.
import pygame
import copy
from Other import coordinatetransformer as ct
from typing import Tuple

#kickPlayer: State + Color -> State
#Purpose: Returns a state where the player representing the given Color
#is removed from the game and all of their penguins are removed.
def kickPlayer(state: State, player: Player):
    for penguin in player.PLACES():
        x,y = penguin
        state.del_penguin(x,y)
    state.remove_cheater(player.COLOR())
    return state
#find_winners: List[Player] -> List[Player]
#Purpose: Finds all players tied for highest score.
def find_winners(player_list: List[Player]):
    winners = [player_list[0]]
    for player in player_list:
        if player.SCORE() > winners[0].score(): #When this occurs, any previous calculated winners are thrown out.
            winners = [player] #and the new top score becomes the sole winner.
        if (player.SCORE() == winners[0].score()) and (not player is winners[0]):
            winners += [player]
    return winners
class GameTree:
    def __init__(self,start_state:State,traversed_states: List[State]):
        self.start_state = start_state
        self.states = traversed_states
    #STATE:
    #STATE: -> State
    #Purpose: Returns the current State of the game tree
    def CURRENT_STATE(self):
        return self.state
    #ACTION: -> State or Error
    #Purpose: Determines the Legality of a move by returning the state
    # that results or elevating an exception raised by cheating.
    @staticmethod
    def ACTION(S: State,A: Callable,**kwargs)->State:
        try:
            a_copy = copy.deepcopy(S)
            A(a_copy,kwargs) #perform action
            a_copy.update() #update turn order
            return a_copy
        except PlayerCheatException as PC:
            raise PlayerCheatException(PC.message)
    #STATEMAP: State -> List[States] or State
    #Purpose: Returns the direct children of the given state.
    @staticmethod
    def STATEMAP(S: State)->List[State]:
        try:    
            if S.PHASE() == Phase.PLACEMENT:
                return [GameTree.ACTION(S=S,A=place_penguin,kwargs={'player':S.CURRENT_PLAYER(),'x':tile.X(),'y':tile.Y()}) for tile in S.BOARD().getTiles()]
            elif S.PHASE() == Phase.PLAY:
                return [GameTree.ACTION(S=S,A=move_penguin,
                                        kwargs={ #"Wouldn't a loop be clearer than a comprehension?" Yeah, but comprehensions are faster in Python.
                                        #You know what would be clearer and just as fast? If I did the project in Typed Racket or Haskell. :(
                                            'player':S.CURRENT_PLAYER(), #Owner of Penguin to be moved
                                            'start_x':place[0], #Penguin start x
                                            'start_y':place[1], #Penguin start y
                                            'end_x':tile[0], #Penguin end x
                                            'end_y':tile[1]}) #Penguin end y
                                            for place in S.CURRENT_PLAYER().PLACES() for tile in S.BOARD().reachable_indexes(*place)]
                                            #For loop: make List[State] containing each State succeeding from valid penguin moves for the given player.
            else:
                successor = S
                for player in S.PLAYERS():
                    if player not in find_winners(S.Players()):
                        successor = kickPlayer(successor)
                return successor
        except PlayerCheatException: #I'm actually going to handle a cheat exception here because this just maps the successor states to the game.
            pass #The GameTree is not a player, and therefore cannot cheat.
    #MOVEGENERATOR: State -> Generator(States)
    #Purpose: For the purposes of matching a proposed state
    #to a valid game state, a generator expression is far more effecient
    #in Python since Generators generate values on the fly and throw them out as needed.
    #Likewise, finding a match early in generation beats a list comprehension, whose evaluation occurs
    #only after the list comprehension is completed.
    @staticmethod
    def MOVEGENERATOR(S: State):
        for place in S.CURRENT_PLAYER().PLACES():
            for tile in S.BOARD().reachable_indexes():
                yield GameTree.ACTION(S=S,A=move_penguin,kwargs={'player':S.CURRENT_PLAYER(),'start_x':place[0],'start_y':place[1],'end_x':tile[0],'end_y':tile[1]})
    #PLACEGENERATOR: State -> Generator(States)
    #Purpose: Generator for seeing if a player attempts to place a penguin on a valid tile.
    @staticmethod
    def PLACEGENERATOR(S:State):
        for tile in S.BOARD().getTiles():
            if tile.vacant():
                yield GameTree.ACTION(S=S,A=place_penguin,kwargs={'player':S.CURRENT_PLAYER(),'x':tile.X(),'y':tile.Y()})
    
    #check_move_legality: MoveResponseQuery -> State or PlayerCheatException
    #Purpose: checks the validity of a given move by attempting to find it among valid successor states to the current state
    def check_move_legality(self,MRQ:Tuple[State,Tuple[int,int],Tuple[int,int]]):
        S, start, end = MRQ
        start_x, start_y = start
        end_x, end_y = end
        try:
            proposed = GameTree.ACTION(S=S,A=move_penguin,kwargs={'player':S.CURRENT_PLAYER(),'start_x':start_x,'start_y':start_y,'end_x':end_x,'end_y':end_y})
            if proposed in GameTree.MOVEGENERATOR(self.states[0]):
                return proposed
            else:
                raise PlayerCheatException(self.states[0].CURRENT_PLAYER().COLOR())
        except (PlayerCheatException,AttributeError,KeyError,IndexError):
            raise PlayerCheatException(self.states[0].CURRENT_PLAYER().COLOR())#Signals player's move is invalid, thus illegal.
    #check_placement_legality: MoveResponseQuery -> State or PlayerCheatException
    #Purpose: Determines legality of placing a penguin.
    def check_placement_legality(self,MRQ:Tuple[State,Tuple[int,int]]):
        state, coord = MRQ
        x,y = coord
        try:
            proposed = GameTree.ACTION(S=state,A=place_penguin,kwargs={'player':state.CURRENT_PLAYER(),'x':x,'y':y})
            if proposed in GameTree.PLACEGENERATOR(self.states[0]):
                return proposed
            else:
                raise PlayerCheatException(self.states[0].CURRENT_PLAYER().COLOR())
        except (PlayerCheatException,AttributeError,KeyError,IndexError):
            raise PlayerCheatException(self.states[0].CURRENT_PLAYER().COLOR())
    #check_legality: MRQ -> State or PlayerCheatException
    #Purpose: Determines legality of placing AND moving penguins
    def check_legality(self,MRQ:Tuple[State,Tuple[int,int] or Tuple[State,Tuple[int,int],Tuple[int,int]]]):
            if self.states[0].PHASE()==Phase.PLACEMENT:
                return GameTree.check_placement_legality(MRQ)
            elif self.states[0].PHASE()==Phase.PLAY:
                return GameTree.check_move_legality(MRQ)
            else:
                NotImplemented#Not mandatory; is win-loss gamestate (List of Placements and details about Win, Loss, or Kick)
#demarshal_query: Dict -> GameTree
#Purpose: Converts the given dictionary into
#an actionable query for the game tree, if able.
def demarshal_query(move_response_query: Dict)->Tuple[State,Tuple[int,int],Tuple[int,int]]:
    return (demarshal_state(move_response_query.get("state")),
            ct.coordinate_transform(move_response_query.get("from"),
                                    ct.coordinate_transform(move_response_query.get("to"))))