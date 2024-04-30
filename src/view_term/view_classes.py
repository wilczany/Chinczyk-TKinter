from enum import Enum

import scrap_engine as se
from termcolor import colored


class Base(se.Frame):
    cords = [(2, 1), (2, 3), (4, 1), (4, 3)]

    def __init__(self, color: int, state: str = "float"):
        self.pawns = []
        self.pawns_count = 0

        corner = get_colored(color, "+")
        hchar = get_colored(color, "-")
        vchar = get_colored(color, "|")

        super().__init__(5, 7, corner_chars=(corner, corner, corner, corner),
                         horizontal_chars=(hchar, hchar), vertical_chars=(vchar, vchar),
                         state=state)

    def add_pawn(self, pawn):
        self.pawns.append(pawn)
        super().add_ob(pawn, self.cords[self.pawns_count][0], self.cords[self.pawns_count][1])
        self.pawns_count += 1

    def remove_pawn(self):
        self.pawns_count -= 1
        p = self.pawns.pop()
        super().rem_ob(p)
        p.remove()
        return p

    def cursor_switch(self):
        if self.pawns_count > 0:
            self.pawns[self.pawns_count - 1].cursor_switch()


class Tile(se.Frame):

    def __init__(self, color: int = None, Home: bool = False):
        self.pawn = None
        self.is_home = Home

        if color is None:
            super().__init__(3, 5, state="float")
        else:
            if not Home:
                super().__init__(3, 5,
                                 corner_chars=(get_colored(color, '+'), get_colored(color, '+'),
                                               get_colored(color, '+'), get_colored(color, '+')),
                                 horizontal_chars=(get_colored(color, '-'), get_colored(color, '-')),
                                 vertical_chars=(get_colored(color, '|'), get_colored(color, '|')),
                                 )
            else:
                star = get_colored(color, "*")
                super().__init__(3, 5, corner_chars=(star, star, star, star),
                                 horizontal_chars=(star, star), vertical_chars=(star, star),
                                 state="float")

    def add_pawn(self, pawn):
        self.pawn = pawn
        super().add_ob(self.pawn, 2, 1)

    def remove_pawn(self):
        tmp = self.pawn
        super().rem_ob(self.pawn)
        self.pawn.remove()
        self.pawn = None

        return tmp

    def cursor_switch(self):
        if self.pawn is not None:
            self.pawn.cursor_switch()
        else:
            raise TabError("Tile is empty:" + str(self.is_home))


# class HomeLineTile(se.Frame):
#     def __init__(self, color: int, state: str = "float"):


class Pawn(se.Object):
    chars = {0: "G", 1: "B", 2: "R", 3: "Y"}

    def __init__(self, color: int, ):

        self.color = color
        self.cursor = False
        super().__init__(get_colored(color, self.chars[color]))

    def cursor_switch(self):
        if self.cursor:
            self.cursor = False
            self.rechar(get_colored(self.color, self.chars[self.color]))
        else:
            self.cursor = True
            self.rechar(get_colored(self.color, self.chars[self.color], "on_light_grey"))

    def action(self, ob):
        pass


def get_colored(color: int, char: str, bg=None):
    match color:
        case 0:
            return colored(char, "green", bg)
        case 1:
            return colored(char, "magenta", bg)
        case 2:
            return colored(char, "red", bg)
        case 3:
            return colored(char, "yellow", bg)


class Message(Enum):
    THROW_DICE = " Wciśnij spację aby rzucić kostką"
    NO_MOVES = " Brak możliwych ruchów"
    EXTRA_TURN = "Wyrzuciłeś 6. Zyskujesz dodatkowy ruch"
    LOST_TURN = "Wyrzuciłeś 3 razy 6. Tracisz kolejkę"
    PLAYER_TURN = "Ruch gracza {} : "
    CHOOSE = "Wybierz pionek używając strzałek. Zatwierdź spacją"
    WINNER = "Wygrał gracz {}"


class TextFrame(se.Frame):
    player_turn = "Ruch gracza {} : "
    def __init__(self):
        super().__init__(22, 40, state="float", corner_chars=["┌", "┐", "└", "┘"],
                         horizontal_chars=["-", "-"],
                         vertical_chars=["|", "|"])

        self.text = se.Text("Chincyk", "float")
        self.add_ob(self.text, 5, 2)
        self.dice = se.Text(DICE2)
        self.add_ob(self.dice, 13, 13)


    def dice_show(self, dice: int):
        match dice:
            case 1:
                self.dice.rechar(DICE1)
            case 2:
                self.dice.rechar(DICE2)
            case 3:
                self.dice.rechar(DICE3)
            case 4:
                self.dice.rechar(DICE4)
            case 5:
                self.dice.rechar(DICE5)
            case 6:
                self.dice.rechar(DICE6)

    def display_message(self, typ: Message, addr: str = None):
        if typ == Message.PLAYER_TURN or typ == Message.WINNER:
            text = typ.value.format(addr)
            self.text.rechar(text)
        else:
            self.text.rechar(typ.value)


DICE1 = r"""  ___________
 |           |
 |           |
 |     O     |
 |           |
 |___________|"""

DICE2 = r""" ___________
|          |
|       O  |
|          |
|  O       |
|__________|"""

DICE3 = r""" ___________
|          |
|       O  |
|     O    |
|  O       |
|__________|"""

DICE4 = r""" ___________
|          |
|  O    O  |
|          |
|  O    O  |
|__________|"""

DICE5 = r""" ___________
|          |
|  O    O  |
|     O    |
|  O    O  |
|__________|"""

DICE6 = r""" ____________
 |          |
 |  O    O  |
 |  O    O  |
 |  O    O  |
 |__________|"""
CENTER = r"""  __________
 /         /\
/_Center!_/  \
| # ___ # |  |
|___| |___|__|"""
