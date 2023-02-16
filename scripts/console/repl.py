import io
import os
import sys
import wotdbg

class Repl:
    def __init__(self, response_callback):
        self.__response_callback = response_callback
        wotdbg.echo = self.__echo
        self.local_vars = { 'echo': self.__echo, 'wotdbg': wotdbg }

    def __echo(self, msg):
        if msg is None:
            return
        self.__response_callback(str(msg))

    def __repl(self, data):
        if data is None or len(data) == 0:
            return None

        stdout_bak = sys.stdout
        stdin_bak = sys.stdin

        try:
            buffer = io.BytesIO()
            sys.stdout = buffer
            sys.stdin = open(os.devnull, 'r')
            try:
                result = str(eval(data, self.local_vars))
            except SyntaxError:
                exec data in self.local_vars
                result = ''
        except Exception:
            import traceback
            result = traceback.format_exc()
        finally:
            sys.stdin = stdin_bak
            sys.stdout = stdout_bak
            if len(result) == 0:
                if len(buffer.getvalue()) == 0:
                    result = None
                else:
                    result = buffer.getvalue()
            else:
                if len(buffer.getvalue()) > 0:
                    result += '\n' + buffer.getvalue()
        return result

    def command(self, prompt):
        self.__echo(self.__repl(prompt.strip()))
