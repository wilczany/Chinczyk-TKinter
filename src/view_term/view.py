import scrap_engine as se
import colorama
import src.view_term.view_classes as vc
from math import floor
from typing import List


class GameView:
    def __init__(self, players: int):
        self.track_cords = []
        self.track = []
        self.starting_tiles = []
        # [0] : green
        # [1] : blue
        # [2] : red
        # [3] : yellow

        self.home_lines: List[List[vc.Tile]] = [[] for _ in range(4)]
        self.pawns = [[] for _ in range(players)]

        self.base = []

        self.cursor_pos = None

        colorama.init()
        # initiate map

        self.screen = se.Map(background=" ")
        with open("resources/track.txt") as file:
            for line in file:
                self.track_cords.append(tuple(line.strip().split(' : ')))

        # draw track

        for i in range(len(self.track_cords)):
            if i == 0:
                tile = vc.Tile(0)
                self.starting_tiles.append(tile)
            elif i % 10 == 0:
                x = i / 10
                if x == 1:
                    tile = vc.Tile(2)
                    self.starting_tiles.insert(2, tile)
                elif x == 2:
                    tile = vc.Tile(1)
                    self.starting_tiles.insert(1, tile)
                else:
                    tile = vc.Tile(3)
                    self.starting_tiles.append(tile)
            else:
                tile = vc.Tile()
            tile.add(self.screen, int(self.track_cords[i][0]), int(self.track_cords[i][1]))
            self.track.append(tile)

        # draw inner track

        with open("resources/home_tracks.txt") as file:
            for count, line in enumerate(file):
                x, y = line.strip().split(' : ')
                tile = vc.Tile(floor(count / 4), True)

                tile.add(self.screen, int(x), int(y))
                self.home_lines[floor(count / 4)].append(tile)

        finish = se.Frame(3, 5, corner_chars=("╔", "╗", "╚", "╝"), state="solid")
        finish.add(self.screen, 20, 12)

        # draw base

        with open("resources/home_base.txt") as file:
            for count, line in enumerate(file):
                x, y = line.strip().split(' : ')
                self.base.append(vc.Base(count))
                self.base[count].add(self.screen, int(x), int(y))

        # draw pawns

        for i in range(players):
            for j in range(4):
                pawn = vc.Pawn(i)
                self.pawns[i].append(pawn)
                self.base[i].add_pawn(pawn)

        self.text_frame = vc.TextFrame()
        self.text_frame.add(self.screen, 52, 3)

        # self.dice = se.Object(vc.DICE)
        # self.dice.add(self.screen, 52, 10)

        self.screen.show()

        # return track, home_lines, finish, pawns

    def move_on_track(self, tile_out: int, tile_in: int):
        if self.track[tile_in].pawn is not None:
            self.move_to_base(tile_in)
        pwn = self.track[tile_out].remove_pawn()
        self.track[tile_in].add_pawn(pwn)
        self.screen.show()

    def move_from_base(self, color: int):
        pwn = self.base[color].remove_pawn()
        # self.track[tile].add_pawn(pwn)
        self.starting_tiles[color].add_pawn(pwn)
        self.screen.show()

    def move_to_home(self, color, tile_out, tile_in):
        pwn = self.track[tile_out].remove_pawn()
        self.home_lines[color][tile_in].add_pawn(pwn)
        self.screen.show()

    def move_from_h_to_h(self, color, tile_out, tile_in):
        pwn = self.track[tile_out].remove_pawn()
        self.home_lines[color][tile_in].add_pawn(pwn)
        self.screen.show()

    def finish(self, color: int, tile: int, at_home: bool):
        if at_home:
            pwn = self.home_lines[color][tile].remove_pawn()
        else:
            pwn = self.track[tile].remove_pawn()

        self.screen.show()

        # add 1 point to player

    def move_to_base(self, tile):
        pwn = self.track[tile].remove_pawn()
        self.base[pwn.color].add_pawn(pwn)

        # czy potrzebne?
        self.screen.show()

    def set_cursor(self, tile_selected: int, color_home=None):
        if self.cursor_pos is not None:
            self.cursor_pos.cursor_switch()

        if tile_selected == -1:
            if color_home is None:
                raise ValueError("color_home cannot be None if tile_selected is -1")
            self.set_cursor_base(color_home)
            return
        elif color_home is not None:
            self.cursor_pos = self.home_lines[color_home][tile_selected]
        else:
            self.cursor_pos = self.track[tile_selected]

        if self.cursor_pos == None:
            raise KeyError("K")
        self.cursor_pos.cursor_switch()
        self.screen.show()

    def set_cursor_base(self, color: int):

        self.cursor_pos = self.base[color]
        self.cursor_pos.cursor_switch()
        self.screen.show()

    def remove_cursor(self):
        self.cursor_pos.cursor_switch()
        self.cursor_pos = None
        self.screen.show()

    def dice_show(self, dice: int):
        self.text_frame.dice_show(dice)
        self.screen.show()

    def display_message(self, typ: vc.Message, addr: str = None):

        self.text_frame.display_message(typ, addr)
        self.screen.show()
