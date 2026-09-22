class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.display = "0"
        self._current_val = 0.0  # The running total
        self._operand = "0"      # The number currently being typed
        self._operator = None     # The pending operator
        self._is_result_shown = False
        self._error_state = False
        self._has_started_operand = False # To distinguish between starting fresh and typing 0

    def _format_display(self, value):
        if isinstance(value, str):
            return value
        try:
            s = format(round(float(value), 10), ".10f").rstrip("0").rstrip(".")
            if s == "" or s == "-0":
                s = "0"
            return s
        except (TypeError, ValueError):
            return "0"

    def press(self, key: str) -> str:
        if self._error_state:
            if key == "C":
                self.reset()
                return self.display
            return self.display

        if key == "C":
            self.reset()
            return self.display

        if key == "BS":
            if self._is_result_shown:
                return self.display
            if len(self._operand) > 1:
                self._operand = self._operand[:-1]
            else:
                self._operand = "0"
            self.display = self._operand
            return self.display

        if key in "0123456789":
            if self._is_result_shown:
                self._current_val = 0.0
                self._operand = "0"
                self._operator = None
                self._is_result_shown = False
                self._has_started_operand = False
            if not self._has_started_operand:
                self._operand = key
                self._has_started_operand = key != "0"
            elif len(self._operand.replace(".", "").replace("-", "")) < 12:
                self._operand += key
            self.display = self._operand
            return self.display

        if key == ".":
            if self._is_result_shown:
                self._current_val = 0.0
                self._operand = "0"
                self._operator = None
                self._is_result_shown = False
                self._has_started_operand = False
            if "." not in self._operand:
                self._operand = self._operand + "." if self._has_started_operand else "0."
                self._has_started_operand = True
            self.display = self._operand
            return self.display

        if key == "+/-":
            if self._is_result_shown:
                self._current_val *= -1
                self.display = self._format_display(self._current_val)
            elif self._operand != "0":
                self._operand = self._operand[1:] if self._operand.startswith("-") else "-" + self._operand
                self.display = self._operand
            return self.display

        if key == "%":
            if self._is_result_shown:
                self._current_val /= 100
                self.display = self._format_display(self._current_val)
            else:
                self._operand = self._format_display(float(self._operand) / 100)
                self.display = self._operand
            return self.display

        if key in "+-*/":
            value = float(self._operand)
            if self._operator is not None:
                if not self._apply(value):
                    return self.display
            else:
                self._current_val = value
            self._operator = key
            self._operand = "0"
            self._has_started_operand = False
            self._is_result_shown = False
            self.display = self._format_display(self._current_val)
            return self.display

        if key == "=":
            if self._operator is not None:
                if not self._apply(float(self._operand)):
                    return self.display
                self._operator = None
                self._operand = self._format_display(self._current_val)
                self._is_result_shown = True
                self.display = self._operand
            return self.display

        return self.display

    def _apply(self, value):
        if self._operator == "+":
            self._current_val += value
        elif self._operator == "-":
            self._current_val -= value
        elif self._operator == "*":
            self._current_val *= value
        elif self._operator == "/":
            if value == 0:
                self.display = "0으로 나눌 수 없습니다"
                self._error_state = True
                return False
            self._current_val /= value
        return True