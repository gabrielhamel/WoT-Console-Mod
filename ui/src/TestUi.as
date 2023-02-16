package
{
    import net.wg.infrastructure.base.AbstractWindowView;
    import scaleform.clik.managers.FocusHandler;
    import flash.events.KeyboardEvent;
    import flash.ui.Keyboard;
    import net.wg.gui.components.controls.TextInput;

    public class TestUi extends AbstractWindowView
    {
        private var commandPrompt: TextInput;
        private var commandOutput: TextInput;
        public var onMessage: Function;

        private final function handleKeyDown(event: KeyboardEvent): void
        {
            if (event.keyCode === Keyboard.ENTER) {
                this.commandOutput.textField.appendText(this.commandPrompt.text + "\r");
                this.commandOutput.textField.scrollV = this.commandOutput.textField.maxScrollV;

                this.onMessage(this.commandPrompt.text);
                this.commandPrompt.text = ""
            }
        }

        public final function logResult(out: String): void
        {
            if (out.charAt(out.length - 1) == "\n") {
                out = out.substr(0, out.length - 1);
            }
            this.commandOutput.textField.appendText(out + "\r");
            this.commandOutput.textField.scrollV = this.commandOutput.textField.maxScrollV;
        }

        override protected function onPopulate() : void
        {
            super.onPopulate();
            this.window.title = "Console";
            this.width = 700
            this.height = 400

            this.addEventListener(KeyboardEvent.KEY_DOWN, this.handleKeyDown, false, 0, true);

            this.commandPrompt = addChild(App.utils.classFactory.getComponent("TextInput", TextInput, {
                x: 0,
                width: width
            })) as TextInput;
            this.commandPrompt.y = this.height - this.commandPrompt.height;

            this.commandOutput = addChild(App.utils.classFactory.getComponent("TextInput", TextInput, {
                x: 0,
                y: 0,
                width: this.width,
                height: this.commandPrompt.y,
                editable: false
            })) as TextInput;

            this.commandOutput.textField.wordWrap = true;

            FocusHandler.getInstance().setFocus(this.commandPrompt);
        }
    }
}
