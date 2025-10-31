import time
from abc import ABC, abstractmethod

from settings import OUTPUT_MODE


class OutputSpace(ABC):
    @abstractmethod
    def write(self, text: str) -> None:
        """Виводимо текст у "відкритий простір"""
        pass


class ConsoleOutput(OutputSpace):
    def write(self, *args, **kwargs) -> None:
        text = " ".join(str(a) for a in args)
        time.sleep(1)
        print(text, **kwargs)


class WebOutput(OutputSpace):
    def write(self, *args, **kwargs) -> None:
        text = " ".join(str(a) for a in args)
        print(text, **kwargs)


match OUTPUT_MODE:
    case "gui":
        ui = WebOutput()
    case "console":
        ui = ConsoleOutput()
    case _:
        ui = ConsoleOutput()
