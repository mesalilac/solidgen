from click import echo, style
from enum import IntEnum
import time


class LogLevel(IntEnum):
    ALL = 0
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    OFF = 100


class Logger:
    def __init__(self, level: LogLevel = LogLevel.ALL):
        self.level = level
        self.width = 9

    def _format_log(self, level, msg, color) -> str:
        padded_level = level.center(self.width)
        timestamp = style(time.strftime("%Y-%m-%d_%H:%M:%S"), fg="bright_black")

        prefix = f"{timestamp}" + " " + "[" + style(padded_level, fg=color) + "]"
        message = style(msg, fg="white")

        return prefix + " " + message

    def debug(self, msg) -> None:
        if LogLevel.DEBUG >= self.level:
            echo(self._format_log("DEBUG", msg, "cyan"))

    def info(self, msg) -> None:
        if LogLevel.INFO >= self.level:
            echo(self._format_log("INFO", msg, "blue"))

    def success(self, msg) -> None:
        if LogLevel.SUCCESS >= self.level:
            echo(self._format_log("SUCCESS", msg, "green"))

    def warning(self, msg) -> None:
        if LogLevel.WARNING >= self.level:
            echo(self._format_log("WARNING", msg, "yellow"))

    def error(self, msg) -> None:
        if LogLevel.ERROR >= self.level:
            echo(self._format_log("ERROR", msg, "red"), err=True)


logger = Logger()
