import subprocess
import time
from collections.abc import Generator
from pathlib import Path
import typing as tp
from contextlib import contextmanager


TASK_FOLDER = Path(__file__).parent
TEST_SERVER_FOLDER = TASK_FOLDER / 'socket_test_servers'
CLIENT_FILE_FULL_PATH = str(TASK_FOLDER / 'client.py')


@contextmanager
def run_socket_server(filename: str | Path, *args: tp.Any) -> Generator[None, None, None]:
    proc = subprocess.Popen(
        ['python', filename, *args],
    )
    time.sleep(0.5)  # a little sleep in order for the server to rise
    yield
    proc.kill()
    time.sleep(0.5)  # a little sleep in order for the server to fall down


def test_run_client_without_server() -> None:
    run = subprocess.run(
        ['python', CLIENT_FILE_FULL_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert run.returncode != 0
    assert b'Connection refused' in run.stderr


def test_first_step_win_server() -> None:
    """Simple server, where player win after first step"""
    with run_socket_server(TEST_SERVER_FOLDER / 'first_step_win_server.py'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')

        assert run.returncode == 0

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'hello' in stdout
        assert 'PLAY' in stdout
        assert 'MESSAGE' in stdout
        assert 'lol' in stdout
        assert 'PLAYER_VICTORY' in stdout


def test_first_step_lose_server() -> None:
    """Simple server, where player lose after first step"""
    with run_socket_server(TEST_SERVER_FOLDER / 'first_step_lose_server.py'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')

        assert run.returncode != 0

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'lose' in stdout
        assert 'PLAY' in stdout
        assert 'MESSAGE' in stdout
        assert 'lol' in stdout
        assert 'PLAYER_DEFEAT' in stdout


def test_win_after_n_iterations_server() -> None:
    """Simple server, where player win after n steps"""
    with run_socket_server(TEST_SERVER_FOLDER / 'win_after_n_iterations_server.py'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')

        assert run.returncode == 0

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'wait' in stdout
        assert 'PLAY' in stdout
        assert 'PLAYER_VICTORY' in stdout


def test_never_win_server() -> None:
    """Simple server, where player can not win and should SURRENDER somewhere"""
    with run_socket_server(TEST_SERVER_FOLDER / 'never_win_server.py'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')

        assert run.returncode != 0

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'long' in stdout
        assert 'PLAY' in stdout
        assert 'SURRENDER' in stdout
        assert 'PLAYER_DEFEAT' in stdout


# @pytest.mark.parametrize('game_server_memory', [10, 100, 1000, 5000])
# def test_custom_server(game_server_memory: int) -> None:
#     """Custom server to test against. Have limited memory, so can be defeated. Private tests run save test cases."""
#     with run_socket_server(TASK_FOLDER / 'server.py', f'--game-server-memory={game_server_memory}'):
#         run = subprocess.run(
#             ['python', CLIENT_FILE_FULL_PATH],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )
#         stdout = run.stdout.decode('utf-8')
#
#         assert run.returncode == 0
#
#         # check logging works somehow
#         assert 'WELCOME' in stdout
#         assert 'PLAY' in stdout
#         assert 'PLAYER_VICTORY' in stdout
