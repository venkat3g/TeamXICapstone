class GameController:
    def __init__(self, game, currentPlayer):
        self.game = game
        self.currentPlayer = currentPlayer
        self.turn = 1 # start at player one's turn
        self._notifyOtherPlayerCallback = None

    def setNotifyOtherPlayerCallback(self, callback):
        self._notifyOtherPlayerCallback = callback

    def getStatusText(self):
        playerSymbol = self.game.hasWon()
        if playerSymbol != 0:
            return "Player %d has won" % self.game.getPlayerFromSymbol(playerSymbol)
        elif self.turn == self.currentPlayer:
            return "Your turn Player %d" % self.turn
        else:
            return "Waiting on Player %d" % self.turn

    def isMyTurn(self):
        return self.turn == self.currentPlayer

    def updateBoard(self, position, player=None):
        valid = False
        if player is None:
            player = self.currentPlayer

        if self.turn == player:
            valid = self.game.playerPicks(player, position)
            if valid:
                # increment turn
                # player 1
                #   -> (1 % 2) = 1 + 1 = 2
                # player 2
                #   -> (2 % 2) = 0 + 1 = 2
                self.turn = (player % 2) + 1
                # notify other player
                if player == self.currentPlayer:
                    self.notifyOtherPlayer(position)
        else:
            print("Player %d attempted to make a move too early" % player)
        
        return valid

    def getSymbolFromBoard(self, position):
        return self.game.getSymbol(position)

    def notifyOtherPlayer(self, position):
        if self._notifyOtherPlayerCallback:
            self._notifyOtherPlayerCallback(position)