import logging


class Colors:
    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#256-colors
    FORM = "\u001b[38;5;{}m"
    MAP = dict(
        black=0,
        white=255,
        grey=245,
        blue=75,
        peach=9,
        yellow=220,
        orange=130,
        red=160,
        bright_red=196,
        magenta=200,
        bright_magenta=207,
        reset="",
    )

    def __init__(self):
        self.__load()

    def __load(self):
        for color in self.MAP:
            setattr(self, color, self.FORM.format(self.MAP[color]))


class Default(logging.Formatter, Colors):
    colors = Colors()
    # format = "%(module)s.%(funcName)s ► %(message)s"
    format = "► %(asctime)s - %(levelname)s │➡ %(message)s"  # log message format
    # format = "► %(message)s"

    FORMATS = {
        logging.DEBUG: f"{colors.grey}{format}{colors.reset}",
        logging.INFO: f"{colors.blue}{format}{colors.reset}",
        logging.WARNING: f"{colors.yellow}{format}{colors.reset}",
        logging.ERROR: f"{colors.bright_red}\033[1m{format}\033[0m{colors.reset}",
        logging.CRITICAL: f"{colors.bright_magenta}\033[1m{format}\033[0m{colors.reset}",
    }

    def format(self, record):
        _format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(_format)
        return formatter.format(record)
