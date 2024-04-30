import src.model.Player as P

class Board:
    EMPTY = 0
    OCCUPIED = [1, 2, 3, 4]
    DEBUG = False
    def __init__(self, players_count: int):

        # 0 - empty
        # 1 - green
        # 2 - blue
        # 3 - red
        # 4 - yellow

        self.board = [0 for i in range(40)]  # 40 tiles
        self.home_lines = [[0 for i in range(4)] for j in range(4)]  # 4 home lines
        self.playersCount = players_count
        self.players = [P.Player(P.Color(i)) for i in range(players_count)]

        self.startingTiles = [0, 20, 10, 30]

    def get_players(self):
        return self.playersCount

    def get_moves(self, color: int, dice: int):

        tab = []

        pawns = self.players[color].get_pawns()
        start = self.startingTiles[color]

        # add only one pawn that can move from base to start
        one_from_base = False

        for pawn in pawns:

            if pawn.at_base:

                if dice != 6:
                    continue
                else:
                    if one_from_base:
                        continue
                    elif self.board[start] != self.OCCUPIED[color]:

                        tab.append(pawn)
                        one_from_base = True

                        continue
                    else:
                        continue

            position = pawn.position
            stp = pawn.steps + dice

            if stp > 44:
                # pawn can finish
                continue
            if 44 >= stp >= 40:
                # pawn can move to safe home
                tab.append(pawn)
            else:
                next_position = (position + dice) % 40

                if self.board[next_position] == self.EMPTY:
                    tab.append(pawn)

                # can beat someone else pawn
                elif self.board[next_position] != self.OCCUPIED[color]:
                    tab.append(pawn)


        return tab

    def move(self, color: int, pawn: P.Pawn, dice: int):
        if pawn.at_base:
            if dice != 6:
                raise Exception("Pawn at base but dice != 6")
            pawn.start(self.startingTiles[color])
            self.board[self.startingTiles[color]] = color + 1
            
            return
        else:
            if pawn.next_move_finish(dice) or pawn.next_move_home(dice):
                self.update_position(pawn, color, dice, pawn.at_home)
                
            else:
                self.board[pawn.position] = self.EMPTY
                self.board[(pawn.position + dice) % 40] = color + 1

        pawn.move(dice)

    def knock_out(self, position: int):
        if self.board[position] == self.EMPTY:
            return
        else:
            player = self.board[position] - 1
            self.players[player].pawn_kicked_out(position)

    def update_position(self, pawn: P.Pawn, color: int, dice: int, at_home: bool):
        if at_home:
            self.home_lines[color][pawn.position] = self.EMPTY
            self.home_lines[color][(pawn.position + dice) % 10] = color + 1
        else:
            self.board[pawn.position] = self.EMPTY
            self.board[(pawn.position + dice) % 40] = color + 1

    def move_from_base(self, color: int):
        self.board[self.startingTiles[color]] = color + 1

        self.players[color].pawn_start()
        print("move from base")

    def check_win(self):
        for index, player in enumerate(self.players):
            if all(pawn.Finished for pawn in player.get_pawns()):
                return True, index
        return False, None


