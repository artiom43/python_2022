import socketserver


class TCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class GameHandler(socketserver.StreamRequestHandler):
    def _send(self, message: str) -> None:
        self.wfile.write(f'{message}\n'.encode('utf-8'))

    def setup(self) -> None:
        super(GameHandler, self).setup()
        self._send('WELCOME')
        self._send('PLAY lose')

    def handle(self) -> None:
        try:
            while True:
                command = self.rfile.readline().decode('utf-8').rstrip()
                if command.startswith('PLAY'):
                    self._send('MESSAGE lol')
                    self._send('PLAYER_DEFEAT')
                    break
        except Exception as e:
            print('Exception', e)


if __name__ == '__main__':
    with TCPServer(('', 59898), GameHandler) as server:
        server.serve_forever()
