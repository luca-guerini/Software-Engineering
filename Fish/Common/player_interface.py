from twisted.internet import reactor, protocol
import json

class GameClientProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Connected to the server")

    def dataReceived(self, data):
        # Assuming data received is JSON-encoded game state
        game_state = json.loads(data.decode('utf-8'))
        print("Received game state:", game_state)

        # Make a move (replace this with your move logic)
        move_data = {"move": "your_move_data"}
        self.transport.write(json.dumps(move_data).encode('utf-8'))

    def connectionLost(self, reason):
        print("Connection lost:", reason)

class GameClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return GameClientProtocol()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

if __name__ == '__main__':
    reactor.connectTCP("127.0.0.1", 8888, GameClientFactory())
    reactor.run()
