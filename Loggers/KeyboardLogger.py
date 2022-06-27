from Loggers import *


class KeyboardLogger(Logger):
    EVENTS = {0x100: "key down", 0x101: "key up", 0x104: "key down", 0x105: "key up"}
    LAYOUT = hex(user32.GetKeyboardLayout(0) & (2 ** 16 - 1))

    def __init__(self, handler: any, quit_key: int = None):
        super(KeyboardLogger, self).__init__(LoggerEnum.KEYBOARD.value, quit_key)
        self.handler = handler
        self.shift_pressed = False

    @staticmethod
    def convert_key(key: int):
        return GET_X_LPARAM(key)

    def _process_body(self, nCode, wParam, lParam):
        key = self.convert_key(lParam[0])

        if key == self._quit_input:
            self.stop_listener()

        if self.EVENTS[wParam] == "key down":
            if key == KeyboardCodes.LSHIFT or key == KeyboardCodes.RSHIFT:
                self.shift_pressed = True
            if self.handler:
                self.handler(
                    KeyboardEvent(
                        key,  # key code
                        lParam[1],  # scan code
                        wParam == 260,  # is alt pressed
                        self.shift_pressed,  # is shift pressed
                        self._current_time(),  # current datetime
                        self.LAYOUT,  # keyboard layout
                        self._get_active_window_title()  # window title
                    )
                )
        else:
            if self.convert_key(lParam[0]) == KeyboardCodes.LSHIFT or self.convert_key(
                    lParam[0]) == KeyboardCodes.RSHIFT:
                self.shift_pressed = False
