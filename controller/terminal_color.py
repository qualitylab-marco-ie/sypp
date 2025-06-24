# terminal_color.py

class TerminalColor:
    COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
    }

    @classmethod
    def color_text(cls, text: str, color: str) -> str:
        color_code = cls.COLORS.get(color.lower(), cls.COLORS["reset"])
        bold = cls.COLORS["bold"]
        return f"{bold}{color_code}{text}{cls.COLORS['reset']}"

    @classmethod
    def print_colored(cls, text: str, color: str) -> None:
        print(cls.color_text(text, color))
