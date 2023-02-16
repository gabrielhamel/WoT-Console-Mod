import io
import os
import wotdbg
import sys
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from gui.Scaleform.framework import ViewSettings, WindowLayer, ScopeTemplates, g_entitiesFactories
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.shared.utils.key_mapping import getBigworldNameFromKey
from gui import InputHandler

TEST_WINDOW_ALIAS = 'testUi'
TEST_WINDOW_SWF = 'test/test-ui.swf'

HOST = '127.0.0.1'
PORT = 2222

class TestWindow(AbstractWindowView):
    def __init__(self):
        super(TestWindow, self).__init__()
        wotdbg.echo = self.__echo
        self.local_vars = { 'echo': self.__echo, 'wotdbg': wotdbg }

    def __echo(self, msg):
        if msg is None:
            return
        if self._isDAAPIInited():
            self.flashObject.logResult(str(msg))

    def _populate(self):
        super(TestWindow, self)._populate()

    def __repl(self, data):
        print("data: ", data)

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

    def onMessage(self, message):
        self.__echo(self.__repl(message.strip()))

    def onWindowClose(self):
        self.destroy()


def init():
    settings = ViewSettings(TEST_WINDOW_ALIAS, TestWindow, TEST_WINDOW_SWF, WindowLayer.WINDOW, None, ScopeTemplates.VIEW_SCOPE)
    g_entitiesFactories.addSettings(settings)
    InputHandler.g_instance.onKeyDown += onhandleKeyEvent

def fini():
    InputHandler.g_instance.onKeyDown -= onhandleKeyEvent


def onhandleKeyEvent(event):
    key = getBigworldNameFromKey(event.key)
    if key == 'KEY_F10':
        showWindow()


def showWindow():
    appLoader = dependency.instance(IAppLoader)
    app = appLoader.getDefLobbyApp()
    app.loadView(SFViewLoadParams(TEST_WINDOW_ALIAS))
