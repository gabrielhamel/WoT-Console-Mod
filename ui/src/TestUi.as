package
{
    import net.wg.infrastructure.base.AbstractWindowView;

    public class TestUi extends AbstractWindowView
    {
        private var my_width: Number;
        private var my_height: Number;

        public final function setWidth(value: Number): void
        {
            this.my_width = value;
        }

        public final function setHeight(value: Number): void
        {
            this.my_height = value;
        }

        override protected function onPopulate() : void
        {
            super.onPopulate();
            width = this.my_width;
            height = this.my_height;
            window.title = "Console";
        }
    }
}
