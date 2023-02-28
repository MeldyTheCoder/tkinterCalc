from tkinter import StringVar
from typing import Union
from types import FunctionType

class Calculations:
    def __init__(self):
        self.__value = 0.0
        self.__operation_history = []
        self.__operation_chars = {"divide": "/",
                                  "substract": "-",
                                  "plus": "+",
                                  "multiply": "*"}

        self.operations = list(self.__operation_chars.values())
        self.digits = [i for i in range(10)]
        self.__chars_operations = {val: key for key, val in self.__operation_chars.items()}

        self.__opposite_operations = {"*": "/",
                                      "/": "*",
                                      "+": "-",
                                      "-": "+"}

    def __add_to_history(self, operation: str, operand: Union[int, float]):
        if not(hasattr(self, operation)) and not(isinstance(getattr(self, operation), FunctionType)):
            raise Exception("No such operation.")

        char = self.__operation_chars[operation]
        self.__operation_history.append((char, operand, self.__value))

    def set_value(self, value: Union[int, float]):
        self.__value = value

    def get_func_name_by_operator(self, operator: str):
        return self.__chars_operations[operator]

    def get_operator_by_func(self, func_name: str):
        return self.__operation_chars[func_name]

    def get_opposite_operator(self, operator: str):
        return self.__opposite_operations[operator]

    def undo(self, steps: int = 1):
        for operation in self.__operation_history[-1: (steps*(-1))]:
            operator = self.get_opposite_operator(operation[0])
            func_name = self.get_func_name_by_operator(operator)
            operand = operation[1]
            self.__value = getattr(self, func_name)(operand)
        return self.value

    @property
    def operation_history(self):
        return self.__operation_history


    @property
    def value(self):
        return self.__value

    def divide(self, value: Union[int, float]):
        self.__value /= value
        self.__add_to_history("divide", value)
        return self.value

    def multiply(self, value: Union[int, float]):
        self.__value *= value
        self.__add_to_history("multiply", value)
        return self.value

    def substract(self, value: Union[int, float]):
        self.__value -= value
        self.__add_to_history("substract", value)
        return self.value

    def plus(self, value: Union[int, float]):
        self.__value += value
        self.__add_to_history("plus", value)
        return self.value

    def raw(self, operator: str, value: Union[int, str]):
        if operator not in self.operations:
            return self.value
        func_name = self.get_func_name_by_operator(operator)
        return getattr(self, func_name)(float(value))


