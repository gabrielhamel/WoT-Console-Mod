package
{
    import net.wg.infrastructure.base.AbstractWindowView;
    import scaleform.clik.managers.FocusHandler;
    import flash.events.KeyboardEvent;
    import flash.ui.Keyboard;
    import net.wg.gui.components.controls.TextInput;
    import scaleform.clik.controls.ScrollingList;

    public class TestUi extends AbstractWindowView
    {
        private var commandPrompt: TextInput;
        private var commandOuput: TextInput;
        public var onMessage: Function;

        private final function handleKeyDown(event: KeyboardEvent): void
        {
            if (event.keyCode === Keyboard.ENTER) {
                // TODO fix that
                this.commandOuput.text = "";

                this.commandOuput.appendText(this.commandPrompt.text + "\n");
                this.onMessage(this.commandPrompt.text);
                this.commandPrompt.text = ""
            }
        }

        public final function logResult(out: String): void
        {
            this.commandOuput.appendText(out)
        }

        override protected function onPopulate() : void
        {
            super.onPopulate();
            window.title = "Console";
            width = 700
            height = 400

            this.addEventListener(KeyboardEvent.KEY_DOWN, this.handleKeyDown, false, 0, true);

            commandPrompt = addChild(App.utils.classFactory.getComponent("TextInput", TextInput, {
                x: 0,
                width: width
            })) as TextInput;
            commandPrompt.y = height - commandPrompt.height;

            commandOuput = addChild(App.utils.classFactory.getComponent("TextInput", TextInput, {
                x: 0,
                y: 0,
                width: width,
                height: commandPrompt.y,
                editable: false
            })) as TextInput;

            FocusHandler.getInstance().setFocus(commandPrompt);
        }
    }
}
