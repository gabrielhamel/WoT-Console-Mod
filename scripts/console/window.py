from repl import Repl
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class ConsoleWindow(AbstractWindowView):
    @staticmethod
    def alias():
        return "Console"

    @staticmethod
    def swf():
        return "console.swf"

    def __init__(self):
        self.__repl = Repl(self.__onResponse)
        super(ConsoleWindow, self).__init__()

    def __onResponse(self, content):
        if self._isDAAPIInited():
            self.flashObject.logResult(content)

    def _populate(self):
        super(ConsoleWindow, self)._populate()

    def onMessage(self, message):
        self.__repl.command(message)

    def onWindowClose(self):
        self.destroy()
