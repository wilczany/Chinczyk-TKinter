# from src.controller.view_term.menu import App

if __name__ == "__main__":

    # *******************************
    # *          TESTING            *
    # *******************************


    import src.view.view as v
    import src.model.Board as b

    import src.localGame as localGame
    # menu = m.Menu().run()
    
    players = 4
    game = localGame.LocalGame(players)
    view = v.GameView(4)
    view.play()
    

    # board = b.Board(4)

    # *******************************
    # *          TESTING            *
    # *******************************

    # import src.localGame as localGame
    # import src.view_term.menu as m
    # import curses
    #
    # stdscr = curses.initscr()
    #
    # menu = m.Menu().run()
    # if not m.GameParams.run:
    #     exit(0)
    #
    # arr = m.GameParams().players_names
    #
    # game = localGame.LocalGame(arr)
    # game.start()
