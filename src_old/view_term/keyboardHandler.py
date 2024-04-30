import sys
import time
from enum import Enum, auto



class Action(Enum):
    LEFT = auto()
    RIGHT = auto()
    SELECT = auto()
    HELP = auto()
    EXIT = auto()


class GetUserAction:

    def __init__(self, ):
        self.i = 0
        self.moves = []
        if sys.platform == "win32":
            import msvcrt
        else:
            import tty, termios, select

            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setraw(self.fd)
            time.sleep(0.1)

    def get_action(self) -> Action:
        if sys.platform == "win32":
            import msvcrt
            ch = msvcrt.getch()

            # TODO: CHECK IT
            match ch:
                case b'\xe0':
                    ch = msvcrt.getch()
                    match ch:
                        case b'H':
                            return Action.LEFT
                        case b'P':
                            return Action.RIGHT
                case b' ':
                    return Action.SELECT
                case b'q':
                    return Action.EXIT
                case b'h':
                    return Action.HELP
                case b'?':
                    return Action.HELP
                case b'\x03':
                    raise KeyboardInterrupt
                case _:
                    return Action.EXIT

        else:
            import tty
            import termios
            import select
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            time.sleep(0.1)

            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)

            if rlist:
                ch = sys.stdin.read(1)
                if ord(ch) == 3:
                    print("exit")
                    termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                    raise KeyboardInterrupt
                elif ch == '\x1b':
                    ch = sys.stdin.read(1)  # Read the next character
                    if ch == '[':
                        ch = sys.stdin.read(1)  # Read the character after [
                        if ch == 'A':
                            return Action.RIGHT
                        elif ch == 'B':
                            return Action.LEFT
                        elif ch == 'C':
                            return Action.RIGHT
                        elif ch == 'D':
                            return Action.LEFT
                elif ch == ' ':
                    return Action.SELECT
                elif ch == 'q':
                    return Action.EXIT
                elif ch == 'h':
                    return Action.HELP

    def reset_term(self):
        if sys.platform != "win32":
            import termios
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


def get_user_action():
    if sys.platform == "win32":
        # TODO: implement windows keyboard listener
        pass
    else:
        import tty
        import termios
        import select

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        time.sleep(0.1)

        while True:

            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                ch = sys.stdin.read(1)
                if ord(ch) == 3:
                    print("exit")
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    break
                elif ch == '\x1b':
                    ch = sys.stdin.read(1)  # Read the next character
                    if ch == '[':
                        ch = sys.stdin.read(1)  # Read the character after [
                        if ch == 'A':
                            pass
                            # view_term.
                        elif ch == 'B':
                            print("down")
                        elif ch == 'C':
                            print("right")
                        elif ch == 'D':
                            print("left")
                elif ch == ' ':
                    print('space')


