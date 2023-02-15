from gui.shared import g_eventBus, events
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.framework import ViewSettings, WindowLayer, ScopeTemplates, g_entitiesFactories
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.shared.utils.key_mapping import getBigworldNameFromKey
from gui import InputHandler

TEST_WINDOW_ALIAS = 'testUi'
TEST_WINDOW_SWF = 'test/test-ui.swf'

class TestWindow(AbstractWindowView):
    def __init__(self):
        super(TestWindow, self).__init__()

    def _populate(self):
        if self._isDAAPIInited():
            self.flashObject.setWidth(300)
            self.flashObject.setHeight(300)
        super(TestWindow, self)._populate()

    def onWindowClose(self):
        self.destroy()

def init():
    settings = ViewSettings(TEST_WINDOW_ALIAS, TestWindow, TEST_WINDOW_SWF, WindowLayer.WINDOW, None, ScopeTemplates.VIEW_SCOPE)
    g_entitiesFactories.addSettings(settings)

    InputHandler.g_instance.onKeyDown += onhandleKeyEvent

def onhandleKeyEvent(event):
    key = getBigworldNameFromKey(event.key)
    if key == 'KEY_P':
        showWindow()

def showWindow():
    appLoader = dependency.instance(IAppLoader)
    app = appLoader.getDefLobbyApp()
    app.loadView(SFViewLoadParams(TEST_WINDOW_ALIAS))
