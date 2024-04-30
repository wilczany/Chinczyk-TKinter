import curses

import npyscreen


class GameParams:
    players_count = int()
    players_names_count = 0
    players_names = []
    run = False


class Menu(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm('MAIN', MainForm())
        self.registerForm('PLAYERS_COUNT', PlayerCountForm())
        for player in range(4):
            form = PlayerForm(name='PLAYER{}'.format(player + 1))
            self.registerForm('PLAYER{}'.format(player + 1), form)

    def onCleanExit(self):
        curses.endwin()


class MainForm(npyscreen.ActionFormMinimal):
    choices = ['Graj', 'Wyjdz']

    # choises = ['Graj lokalnie', 'Graj przez siec', 'Wyjdz']

    def create(self):

        self.add(npyscreen.TitleText, name='Witaj w grze Chińczyk', editable=False)
        self.choice = self.add(npyscreen.TitleSelectOne, max_height=4, name='Wybierz opcje',
                               values=self.choices)

    def on_ok(self):
        if self.choice.get_selected_objects()[0] == 'Graj':
            self.parentApp.switchForm('PLAYERS_COUNT')
        else:
            self.parentApp.setNextForm(None)
    
    def on_cancel(self):
        raise self.parentApp.setNextForm(None)


class PlayerCountForm(npyscreen.ActionFormV2, npyscreen.Popup):

    def create(self):
        self.add(npyscreen.TitleText, name="Podaj liczbe graczy", editable=False)
        self.count = self.add(npyscreen.Slider, out_of=4, lowest=2, value=2, name="Gracze")

    def on_ok(self):
        GameParams.players_count = int(self.count.value)
        self.parentApp.setNextForm('PLAYER1')

    def on_cancel(self):
        self.parentApp.switchForm('MAIN')


class PlayerForm(npyscreen.ActionFormV2):

    def create(self):

        self.add(npyscreen.TitleText, name="Podaj imie gracza "
                                           + str(self.name)[-1] + ". :",
                 editable=False)
        self.player_name = self.add(npyscreen.TitleText, name="Imie")

    def on_ok(self):

        name = self.player_name.value
        GameParams.players_names.append(name)
        GameParams.players_names_count += 1
        if GameParams.players_names_count == GameParams.players_count:
            GameParams.run = True
            self.parentApp.setNextForm(None)
        else:
            # self.parentApp.setNextForm('PLAYER{}'.format(GameParams.players_names_count + 1))
            self.parentApp.setNextForm('PLAYER' + str(int(self.name[-1]) + 1))

    def on_cancel(self):
        GameParams.players_names.clear()
        self.parentApp.switchForm('MAIN')
