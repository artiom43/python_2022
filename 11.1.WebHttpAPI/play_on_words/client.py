import socket
import argparse
import sys
# import requests
# from bs4 import BeautifulSoup
from pathlib import Path


FILE_DIR = Path(__file__).parent


def main(freeport: int) -> None:
    # raise NotImplementedError
    # print('sdf')
    # response = requests.get('https://www.mit.edu/~ecprice/wordlist.10000')
    # soup = BeautifulSoup(response.text)
    # html = soup.html
    # print(html)
    # print(type(freeport))
    # with open('words.txt', 'w') as f:
    #     f.write(html.text)
    #     tr = f.read()
    #     print(tr)
    with open('words.txt', 'r') as f:
        data = f.read().split('\n')
        # print(data)

    # print(html, file=FILE_DIR. 'file_with_words')
    # print(html[0])
    # print(socket.getaddrinfo('localhost', 48807, family=socket.AF_INET6, type=socket.SOCK_STREAM))
    # addr = '::1', 59898, 0, 0
    # print("sdfs")
    # print(freeport)
    with socket.socket(
            family=socket.AF_INET,  # Adress Family INET
            type=socket.SOCK_STREAM  # ≈ "use TCP"
    ) as sock:
        try:
            used_words = set()
            sock.connect(('localhost', freeport))
            # return None
            # print(freeport)
            # print("sdf")
            real_response: list[str] = []
            while len(real_response) < 3:
                response = sock.recv(1024)
                for rl in response.split():
                    real_response.append(rl.decode('utf-8'))
                    print(rl.decode('utf-8'))
                # print(response.split(), "response")
            # message = 'ollo'
            # sock.sendall(b"PLAY {message}\n")
            # sock.sendall('{message}\n'.encode('utf-8'))
            used_words.add(real_response[2])
            # print("PLAY ollo\n")
            # print("PLAY " + data[4])
            # return None
            # if 'QUIT' in real_response:
            #     print('QUIT')
            #     return None
            word_to_respond = real_response[2]
            # print(word_to_respond)
            # used_words.add(data[4])
            # return None
            # try:
            # return None
            while True:
                send_word = ""
                for strr in data:
                    if len(strr) > 3 and strr[0] == word_to_respond[-1] and strr not in used_words:
                        send_word = strr
                        break
                # for str in data:
                #     if str.startswith('w'):
                #         print(str, "current_word")
                # print([send_word, 'variant', b"PLAY {send_word}\n"])
                # sock.sendall(b"PLAY ollo\n")
                if send_word == '':
                    # response = sock.recv(1024)
                    # print(response, 'response')
                    # return None
                    # tasl = 'SURRENDER\n'.encode('utf-8')
                    # response = sock.recv(1024)
                    sock.sendall('SURRENDER\n'.encode('utf-8'))
                    print('SURRENDER\n')
                    response = sock.recv(1024)
                    for rl in response.split():
                        print(rl.decode('utf'))
                    return None
                else:
                    # sock.sendall(("PLAY " + send_word + "\n").encode('utf-8'))
                    # print(f"PLAY {send_word}\n")
                    task = f'PLAY {send_word}\n'.encode('utf-8')
                    sock.sendall(f'PLAY {send_word}\n'.encode('utf-8'))
                    print(task.decode('utf-8'))
                    used_words.add(send_word)
                # break
                real_response = []
                i = 0
                # break
                while len(real_response) < 3 and i < 5:
                    response = sock.recv(1024)
                    for rl in response.split():
                        real_response.append(rl.decode('utf-8'))
                    # print(response.split(), "response")
                    i += 1
                # if 'QUIT' in real_response:
                #     print('QUIT')
                #     return None
                print(real_response)
                # break
                if 'PLAYER_VICTORY' in real_response:
                    # print("sdfs")
                    break
                if 'PLAYER_DEFEAT' in real_response:
                    print('PLAYER_DEFEAT')
                    # sock.shutdown(socket.SHUT_RDWR)
                    sock.connect(('localhost', 0))
                    break
                word_to_respond = real_response[2]
                if word_to_respond in used_words:
                    sock.sendall('SURRENDER\n'.encode('utf-8'))
                    print('SURRENDER\n')
                    response = sock.recv(1024)
                    for rl in response.split():
                        print(rl.decode('utf'))
                    sock.connect(('localhost', 0))
                used_words.add(word_to_respond)
                # break
            # except Exception:
            #     pass

            response = sock.recv(1024)
            print(response.split())
            response = sock.recv(1024)
            print(response)
            # response = sock.recv(1024)
            # print(response)
        except KeyboardInterrupt:
            print("QUIT")
            sock.sendall('QUIT'.encode('utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=59898)
    args = parser.parse_args(sys.argv[1:])
    # print(args.port[:-1], int(args.port))
    # print(args.port, args.port.decode())
    main(int(args.port))
