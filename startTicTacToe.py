# TODO: make tic-tac-toe an menu option from GUI Configuration Tool

import gui.tictactoePage as page
from gui.controller.GameController import GameController
from gui.game.tictactoeGame import TicTacToeGame
import time
from random import randint
from gui import ThreadWrapper, PlutoController

playerNumber = 1
game = TicTacToeGame()
controller = GameController(game, playerNumber)

def notifyOtherUser(position):
    PlutoController.sendMsg(str(position))

def readMove(args):
    while not args['done']:

        msg = PlutoController.readRXMessage()

        if msg is not None and len(msg) == 1:
            if controller.turn != controller.currentPlayer:
                position = int(msg)
                valid = controller.updateBoard(position, (controller.currentPlayer % 2) + 1) # other players move
            
                if valid:
                    game_position = filter(lambda x: x[2] == position, page.game_positions)[0]
                    game_position[1].set(controller.getSymbolFromBoard(position)) # update button to reflect updated board
                else:
                    # FIXME: temporarily just update to next player
                    controller.currentPlayer = (controller.currentPlayer % 2) + 1
                    print("Other player attempted to play at position %d" % position)
        
            page.tictactoe_support.playerText.set(controller.getStatusText())


        time.sleep(1)

PlutoController.getSdr() # initializes the Pluto device

PlutoController.readRX = True

collectionThread = ThreadWrapper.ThreadController(PlutoController.plutoRXThread)
updateGUIThread = ThreadWrapper.ThreadController(readMove)

collectionThread.start()
updateGUIThread.start()

controller.setNotifyOtherPlayerCallback(notifyOtherUser)

page.vp_start_gui(controller)

page.vp_start_loop()

collectionThread.stop()
updateGUIThread.stop()

print("done")