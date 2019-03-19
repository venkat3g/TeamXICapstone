import tictactoe
import tictactoe_support

try:
    import Tkinter as tk
    import tkFileDialog as fileDialog
except ImportError:
    import tkinter as tk
    from tkinter import fileDialog
    

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


# list will contain the (TkButton, TkStringVar, int - buttonNumber)
game_positions = []

_gameController = None

def updateGrid(evnt):
    position = filter(lambda x: x[0] == evnt.widget, game_positions)[0]
    buttonText = position[1]

    # check if its our turn
    if _gameController.isMyTurn() and not _gameController.game.hasWon():
        _gameController.updateBoard(position[2])
        buttonText.set(_gameController.getSymbolFromBoard(position[2]))
        tictactoe_support.playerText.set(_gameController.getStatusText())


def vp_start_gui(root, gameController):
    '''Starting point when module is the main routine.'''
    global _gameController, game_positions, w
    (w, top) = tictactoe.create_TicTacToeTL(root)
    
    game_positions = []
    _gameController = gameController
    status = gameController.getStatusText()
    tictactoe_support.playerText.set(status)

    game_positions.append((top.b0, tictactoe_support.b0, 0))
    game_positions.append((top.b1, tictactoe_support.b1, 1))
    game_positions.append((top.b2, tictactoe_support.b2, 2))
    game_positions.append((top.b3, tictactoe_support.b3, 3))
    game_positions.append((top.b4, tictactoe_support.b4, 4))
    game_positions.append((top.b5, tictactoe_support.b5, 5))
    game_positions.append((top.b6, tictactoe_support.b6, 6))
    game_positions.append((top.b7, tictactoe_support.b7, 7))
    game_positions.append((top.b8, tictactoe_support.b8, 8))

    for position in game_positions:
        button = position[0]
        tkStringVar = position[1]

        tkStringVar.set('')
        button.bind('<ButtonRelease-1>', updateGrid)