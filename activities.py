from tkinter import Tk, Label, Entry, Button, Frame, messagebox, W, StringVar
from abc import abstractmethod
from calculations import Calculations

calc = Calculations()

class BaseActivity:
    title = "BaseActivity"

    def __init__(self, root: Tk = None):
        self.root = root if root else Tk()
        self.root.title(self.title)
        self.frame = Frame(self.root, padx=10, pady=10)
        self.frame.pack()
        self._on_start()

    @abstractmethod
    def _on_start(self):
        print("Виджеты не добавлены!")

    @abstractmethod
    def _on_activity_change(self):
        pass

    def mainloop(self, **kwargs):
        return self.root.mainloop(**kwargs)

    def setActivity(self, activity):
        if not issubclass(activity, BaseActivity):
            raise Exception('Not an activity!')
        self._on_activity_change()
        new_activity = activity(self.root)
        return new_activity

class MainActivity(BaseActivity):
    title = "Simple Calculator"

    def digit_button_click(self, number: int):
        pass

    def operation_button_click(self, operation: str):
        if not operation in calc.operations:
            return

    def _on_start(self):
        e = Entry(self.root, width=35, borderwidth=5)
        e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        placements = [{"column": 0, "row": 3}, {"column": 1, "row": 3}, {"column": 2, "row": 3}, {"column": 0, "row": 2}, {"column": 1, "row": 2}, {"column": 2, "row": 2}]
        buttons = [Button(self.root, text=str(digit), padx=40, pady=20, command=lambda *args: self.digit_button_click(digit)) for digit in calc.digits]



