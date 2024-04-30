import tkinter as tk
from src.localGame import LocalGame as Game
from time import sleep
import random

WIDTH = HEIGHT = 812

SQ_SIZE = 50
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pass


class GameView:
    track_coords = []
    base_coords = [(550, 70), (150, 450), (550, 450), (150, 70) ]
    home_coords = [
        [(378, 56), (378, 112), (378, 168), (378, 224)],
        [(378, 504), (378, 448), (378, 392), (378, 336)],
        [(602, 280), (546, 280), (490, 280), (434, 280)],
        [(154, 280), (210, 280), (266, 280), (322, 280)]
    ]
    starting_tiles = [0, 20, 10, 30]
    def __init__(self, players):

        self.player_count = players

        self.player_turn = 0
        
        self.six_in_row = 0

        self.game = Game(players)
        self.root = tk.Tk()
        self.track = []
        self.base = []
        self.home_lines = [[] for _ in range(4)]
        self.dice_value = 0
        colors = ['green', 'blue', 'red', 'yellow']
        self.kolory = ['zielony', 'niebieski', 'czerwony', 'zolty']
        self.pawns = []
        self.base_ico = []
        self.cords()
        for color in colors:
            self.pawns.append(tk.PhotoImage(file=f"resources/pawns/{color}.png"))
            self.base_ico.append(tk.PhotoImage(file=f"resources/base/base_{color}.png"))

        self.root.geometry("812x812")
        self.root.title("Chinczyk")
        self.root.resizable(False, False)

        self.bg = tk.PhotoImage(file="resources/board/board.png")
        background = tk.Label(self.root, image=self.bg)
        background.place(x=0, y=0)

        self.message_box = tk.Label(self.root, text="", font=("Arial", 20), fg="black", bg="#CCAED6")
        self.message_box.pack(pady=20)

        board_frame = tk.Frame(self.root, width=812, height=612)
        background2 = tk.Label(board_frame, image=self.bg)
        background2.place(x=0, y=0)
        board_frame.place(x=0, y=70)
        self.empty = tk.PhotoImage(file="resources/pawns/empty.png")

        for count, c in enumerate(self.track_coords):
            if count % 10 == 0:
                match count // 10:
                    case 0:
                        bt = tk.Button(board_frame, width=SQ_SIZE, height=SQ_SIZE, bg=colors[0], image=self.empty)
                    case 1:
                        bt = tk.Button(board_frame, width=SQ_SIZE, height=SQ_SIZE, bg=colors[2], image=self.empty)
                    case 2:
                        bt = tk.Button(board_frame, width=SQ_SIZE, height=SQ_SIZE, bg=colors[1], image=self.empty)
                    case 3:
                        bt = tk.Button(board_frame, width=SQ_SIZE, height=SQ_SIZE, bg=colors[3], image=self.empty)
                # bt = tk.Button(board_frame, width=SQ_SIZE, height=SQ_SIZE, bg=colors[count // 10], image=self.empty)
            else:
                bt = tk.Button(board_frame, width=SQ_SIZE, height=SQ_SIZE, image=self.empty)
            bt.place(x=c[0], y=c[1])
            self.track.append(bt)

        for count, c in enumerate(self.home_coords):
            for row in c:
                if count == 2:
                    bt = tk.Button(board_frame, width=SQ_SIZE, height=SQ_SIZE, image=self.empty, bg="pink")
                else:
                    bt = tk.Button(board_frame, width=SQ_SIZE, height=SQ_SIZE, image=self.empty,
                                   bg=f"light" + colors[count])
                bt.place(x=row[0], y=row[1])
                self.home_lines[count].append(bt)
                self.track.append(bt)

        for i, cords in enumerate(self.base_coords):
            
            bt = tk.Button(board_frame, width=SQ_SIZE * 2, height=SQ_SIZE * 2, image=self.base_ico[i])
            bt.place(x=cords[0], y=cords[1])
            
            # bt.configure(command=lambda: self.move_from_base(i))
            self.base.append(bt)

        self.dice_img = []

        for i in range(6):
            self.dice_img.append(tk.PhotoImage(file=f"resources/dice/dice_{i + 1}.png"))
        self.dice = tk.Label(self.root, image=self.dice_img[1], height=100, width=100)
        self.dice.place(x=350, y=700)

        self.quit = tk.Button(self.root, text="Quit", width=10, height=2, command=self.root.destroy)
        self.quit.place(x=700, y=720)



    def play(self):

        self.roll = tk.Button(self.root, text="Roll dice", width=10, height=2, command=lambda: self.roll_dice())
        self.roll.place(x=40, y=720)
        self.message_box.configure(text="Ruch gracza: " + self.kolory[self.player_turn])
        self.lock_all()
        self.root.mainloop()
 
    
    def lock_all(self):
        #self.lock_dice()

        for i in range(40):
            self.track[i].configure(state="disabled")
        
        for i in range(4):
            self.base[i].configure(state="disabled")
        
        for color in self.home_lines:
            for tile in color:
                tile.configure(state="disabled")

    def unlock_move(self, tile_selected: int, color):

        if tile_selected == -1:
            if color is None:
                raise ValueError("color_home cannot be None if tile_selected is -1")
            self.unlock_base(color)
            return
        elif tile_selected >= 100:
            self.unlock_home(tile_selected, color)
        else:
            self.unlock_track(tile_selected, color)

    def unlock_base(self, color):
       self.base[color].configure(command=lambda: self.move_from_base(color))
       self.base[color].configure(state="normal")

    def unlock_home(self, tile, color):
        pos = tile - 100
        if pos > 3:
            self.home_lines[color][pos].configure(command=lambda: self.move_to_finish(color, tile))
        else:
            self.home_lines[color][pos].configure(command=lambda: self.move_to_home(color, tile))
    
    def unlock_track(self,tile,color):
        self.track[tile].configure(command=lambda: self.move_on_track(tile, color))
        self.track[tile].configure(state="normal")

    def lock_dice(self):
        self.roll.configure(state="disabled")

    def unlock_dice(self):
        self.roll.configure(state="normal")

    #
    #   Dice and messages
    #    
        
    def set_dice(self, dice):
        self.dice.configure(image=self.dice_img[dice - 1])

    def roll_dice(self):
        
        self.dice_value = self.throw_dice()
        self.set_dice(self.dice_value)
        self.lock_dice()
        moves = self.game.get_possible_moves(self.dice_value, self.player_turn)
        if moves == None:
            self.message_box.configure(text="Brak Mozliwych Ruchow")
            self.message_box.after(1000, self.next_player_turn)

        else:
            
            self.message_box.configure(text="Wybierz pionek")

            for tile in moves:
                self.unlock_move(*tile)

            # self.next_player_turn()
    #
    #   Actions
    # 
    def move_to_home(self, color, tile):
        next_pos = self.game.execute_move(tile, 0, color)
        self.home_lines[color][tile].configure(image=self.empty)
        self.home_lines[color][next_pos].configure( image=self.pawns[self.player_turn])
        self.next_player_turn()


    def move_from_base(self, color):
        
        next_pos = self.game.execute_move(-1, self.dice_value, color)
        self.next_player_turn()
        self.track[next_pos].configure(image=self.pawns[color])    

    
    def move_on_track(self, tile, color):
        next_pos = self.game.execute_move(tile, self.dice_value, color)
        if next_pos >= 100:
            self.track[tile].configure(image=self.empty)
            self.home_lines[color][next_pos - 100].configure(image=self.pawns[color])
        else:
            self.track[tile].configure(image=self.empty)
            self.track[next_pos].configure(image=self.pawns[color])
        self.next_player_turn()
    
    def move_to_finish(self, color, tile):
        next_pos = self.game.execute_move(tile, 0, color)
        if next_pos != 4:
            raise Exception("Pawn not finished")
        self.home_lines[color][tile - 100].configure(image=self.empty)
        self.next_player_turn()
    
    def next_player_turn(self):
        self.lock_all()
        if self.game.is_finished():
            self.message_box.configure(text="Koniec gry")
            self.message_box.after(1000, self.root.destroy)
        if self.dice_value == 6 and self.six_in_row < 2:
            self.six_in_row += 1
        else:
            self.player_turn = (self.player_turn + 1) % self.player_count
            self.six_in_row = 0
        self.message_box.configure(text="Ruch gracza: " + self.kolory[self.player_turn])
        self.message_box.after(500, self.unlock_dice)
        

            
    def cords(self):
        
        x = 434
        y = 0
        space = 56
        
        directions = [(4, 1, 'y'), (4, 1, 'x'), (2, 1, 'y'), (4, -1, 'x'), 
              (4, 1, 'y'), (2, -1, 'x'), (4, -1, 'y'), (4, -1, 'x'), 
              (2, -1, 'y'), (4, 1, 'x'), (4, -1, 'y'), (2, 1,'x')]

        for steps, direction, axis in directions:
            for _ in range(steps):
                self.track_coords.append((x, y))
                
                if axis == 'x':
                    x+= direction * space
                if axis == 'y':
                    y += direction * space
                    
    def throw_dice(self):
        dice = random.randint(1, 6)
        
        return dice
