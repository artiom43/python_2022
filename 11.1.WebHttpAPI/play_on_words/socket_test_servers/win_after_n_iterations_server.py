import socketserver


WIN_STEP = 100


class TCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class GameHandler(socketserver.StreamRequestHandler):
    def _send(self, message: str) -> None:
        self.wfile.write(f'{message}\n'.encode('utf-8'))

    def setup(self) -> None:
        super(GameHandler, self).setup()
        self._send('WELCOME')
        self._send('PLAY wait')

        self._n = 0

    def handle(self) -> None:
        try:
            while True:
                command = self.rfile.readline().decode('utf-8').rstrip()
                if command.startswith('PLAY'):
                    word = command[5:].lower()
                    self._send('VALID')
                    self._n += 1

                    if self._n > WIN_STEP:
                        self._send('PLAYER_VICTORY')
                        break

                    self._send(f'PLAY {word[::-1]}')
        except Exception as e:
            print('Exception', e)


if __name__ == '__main__':
    with TCPServer(('', 59898), GameHandler) as server:
        server.serve_forever()
