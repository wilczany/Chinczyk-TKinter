from enum import IntEnum, IntFlag, Enum


# [0] : green
# [1] : blue
# [2] : red
# [3] : yellow
class Color(Enum):
    GREEN = 0
    BLUE = 1
    RED = 2
    YELLOW = 3


class Player:

    def __init__(self, color: Color):
        self.pawns = [
            Pawn(color.value),
            Pawn(color.value),
            Pawn(color.value),
            Pawn(color.value)
        ]
        self.steps = [0, 0, 0, 0]
        self.start = int()
        self.pieces_at_base = 4
        match color:
            case Color.GREEN:
                self.start = 0
            case Color.BLUE:
                self.start = 20
            case Color.RED:
                self.start = 10
            case Color.YELLOW:
                self.start = 30

    def get_pawns_location(self):
        positions = []
        for p in self.pawns:
            positions.append(p.position)

    def set_pawn_location(self, pawn: int, location: int):

        for i in range(4):
            if self.pawns[i].position == pawn:
                pass

        # or maybe
        # for i in range(4):
        #     if self.pawns[i] == pawn:
        #         self.pawns[i] = location

    def pawn_start(self):

        tmp = [self.start if x == -1 else x for x in self.pawns]

    def pawn_kicked_out(self, position: int):

        for i in range(4):
            if self.pawns[i].position == position:
                self.pawns[i].knocked_out()
                self.pieces_at_base += 1

    def get_pawns(self):
        return self.pawns


class Pawn:

    def __init__(self, color: int):
        self.steps = 0
        self.at_base = True
        self.at_home = False
        self.Finished = False
        self.position = -1
        self.color = color

    def start(self, start: int):
        self.at_base = False
        self.position = start

    def move(self, dice: int):

        if self.next_move_finish(dice):

            self.Finished = True
            self.steps += dice
            self.position += dice
            if self.steps != 44:
                raise Exception("Pawn not finished but steps == 44")
            
        elif self.next_move_home(dice):

            self.at_home = True
            self.steps += dice
            self.position = self.steps % 10
        else:
            self.position = (self.position + dice) % 40
            self.steps += dice
            
    def knocked_out(self):
        self.at_base = True
        self.position = -1
        self.steps = 0

    def can_move(self, dice: int):
        
        if self.at_base:
            return dice == 6
        else:
            return self.steps + dice <= 44

    def next_move_finish(self, dice: int):
        return self.steps + dice == 44

    def next_move_home(self, dice: int):
        return 44 >= self.steps + dice >= 40

