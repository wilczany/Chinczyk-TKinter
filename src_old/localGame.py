import random
import time

from src.model.Board import Board

class LocalGame:


    def __init__(self,players :int):

        
        self.players = players
        
        self.board = Board(self.players)

    
    def start(self):
        pass
    
    def get_possible_moves(self, dice, player):
        possible_moves = self.board.get_moves(player, dice)
        ln = len(possible_moves)
        moves = []
        if ln == 0:
            return None
        
        for pawn in possible_moves:
            if pawn.at_base:
                moves.append([-1, player])
            elif pawn.at_home:
                moves.append([pawn.position +100 , player])
            else:
                moves.append([pawn.position, player ])

        
        return moves
            

    
    def execute_move(self, tile, dice, player):
        
        next_pos = None
        possible_moves = self.board.get_moves(player, dice)
        if tile >= 100:
            for pawn in possible_moves:
                if pawn.at_home and pawn.position == tile - 100:
                    self.board.move(player, pawn, dice)
                    return pawn.position
        
        elif tile == -1:
            for pawn in possible_moves:
                if pawn.at_base:
                    self.board.knock_out(self.board.startingTiles[player])
                    self.board.move(player, pawn, dice)
                    return pawn.position
        else:
            for pawn in possible_moves:
                
                if pawn.position == tile:
                    if pawn.next_move_home(dice):
                        self.board.move(player, pawn, dice)
                        return pawn.position + 100
                    else:
                        next_pos = (pawn.position + dice) % 40
                        self.board.knock_out(next_pos)
                        self.board.move(player, pawn, dice)
                        return pawn.position
                
            raise Exception(f"No pawn on tile({tile})')")      
        
  
    
    def is_finished(self):
        return not self.board.check_win()
    
    def print_board(self):
        board = self.board.board
        print(board)
        # for i, tile in enumerate(board):
            # print(f'{i}: {tile}', end=" ")

            