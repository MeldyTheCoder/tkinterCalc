import tkinter
from abc import abstractmethod
from calculations import Calculations
from typing import Optional, Union

calc = Calculations()

class BaseActivity:
    title = "BaseActivity"

    def __init__(self, root: tkinter.Tk = None):
        self.root = root if root else tkinter.Tk()
        self.root.title(self.title)
        self._on_start()

    @abstractmethod
    def _on_start(self) -> None:
        print("Виджеты не добавлены!")

    @abstractmethod
    def _on_activity_change(self) -> None:
        pass

    def mainloop(self, **kwargs) -> None:
        return self.root.mainloop(**kwargs)

    def set_activity(self, activity):
        if not issubclass(activity, BaseActivity):
            raise Exception('Not an activity!')
        self._on_activity_change()
        new_activity = activity(self.root)
        return new_activity

class MainActivity(BaseActivity):
    title = "Simple Calculator"

    operation_padding = {"+": {"padx": 39, "pady": 20},
                         "-": {"padx": 41, "pady": 20},
                         "*": {"padx": 40, "pady": 20},
                         "/": {"padx": 41, "pady": 20}}

    operation_grids = {"+": {"column": 0, "row": 5},
                       "-": {"column": 0, "row": 6},
                       "*": {"column": 1, "row": 6},
                       "/": {"column": 2, "row": 6}}

    digit_grids = [{"column": column, "row": row} for row in reversed(range(1, 4)) for column in range(0, 3)]
    digit_grids.insert(0, {"column": 0, "row": 4})

    digit_padding = {"padx": 40, "pady": 20}

    entry: tkinter.Entry

    last_operation: str = ""

    def get_operation_padding(self, operator: str) -> Optional[dict]:
        if operator not in calc.operations:
            return
        return self.operation_padding[operator]

    def get_operation_placement(self, operator: str) -> Optional[dict]:
        if operator not in calc.operations:
            return
        return self.operation_grids[operator]

    def digit_button_callback(self, number: int) -> None:
        self.entry.insert(len(self.entry.get()), str(number))

    def clear_callback(self) -> None:
        self.entry.delete(0, tkinter.END)
        calc.set_value(0)

    def operation_button_callback(self, operation: str) -> None:
        if operation not in calc.operations:
            return
        if not self.entry.get():
            return
        entry_text = self.entry.get()
        self.entry.delete(0, tkinter.END)
        if not self.last_operation:
            calc.set_value(int(entry_text))
            self.last_operation = operation
            return
        self.last_operation = operation
        calc.raw(operation, entry_text)


    def get_digit_placement(self, digit: int) -> Optional[dict]:
        if digit not in calc.digits:
            return
        return self.digit_grids[digit]

    def equal_callback(self) -> None:
        if self.last_operation:
            calc.raw(self.last_operation, self.entry.get())
        self.entry.delete(0, tkinter.END)
        value = int(calc.value) if calc.value.is_integer() else calc.value
        self.entry.insert(0, value)
        self.last_operation = ""

    def _on_start(self) -> None:
        self.entry = tkinter.Entry(self.root, width=35, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        for digit in reversed(calc.digits):
            new_func = lambda digit = digit: self.digit_button_callback(digit)
            btn = tkinter.Button(self.root, text=str(digit), command=new_func, **self.digit_padding)
            btn.grid(**self.get_digit_placement(digit))

        for operator in calc.operations:
            new_func = lambda operator = operator: self.operation_button_callback(operator)
            padding = self.get_operation_padding(operator)
            btn = tkinter.Button(self.root, text=operator, **padding, command=new_func)
            btn.grid(**self.get_operation_placement(operator))

        tkinter.Button(self.root, text='Clear', padx=79, pady=20, command=lambda: self.clear_callback()).grid(row=4, column=1, columnspan=2)
        tkinter.Button(self.root, text='=', padx=91, pady=20, command=lambda: self.equal_callback()).grid(row=5, column=1, columnspan=2)

    def _on_activity_change(self) -> None:
        pass


