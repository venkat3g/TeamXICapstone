import tictactoePage as page
from controller.GameController import GameController
from game.tictactoeGame import TicTacToeGame
import time
from random import randint
import ThreadWrapper, PlutoController

def notifyOtherUser(position):
    PlutoController.sendMsg(str(position))

def startTicTacToe(root, playerNumber):
    game = TicTacToeGame()
    controller = GameController(game, playerNumber)

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
                        print("Other player attempted to play at position %d" % position)
            
                page.tictactoe_support.playerText.set(controller.getStatusText())


            time.sleep(1)


    page.vp_start_gui(root, controller)
    
    controller.setNotifyOtherPlayerCallback(notifyOtherUser)

    updateGUIThread = ThreadWrapper.ThreadController(readMove)

    updateGUIThread.start()

    def stopTTT():
        updateGUIThread.stop()
        page.tictactoe.destroy_TicTacToeTL()
        PlutoController.sendMsg("") # Do not send any more Tic-Tac-Toe messages

    page.w.protocol("WM_DELETE_WINDOW", stopTTT)