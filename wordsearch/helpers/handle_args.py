import getopt
from enum import IntEnum


class LevelInt(IntEnum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class HandleArgs:
    """ HandleArgs class """

    def __init__(self, argv):
        """
        Args:
            argv: list of arguments
        """
        self._input_file = ""
        self._level_int = 0
        self._word_list = ""

        level_conv_dict = {"E": 0, "EASY": 0, "M": 1, "MEDIUM": 1, "H": 2, "HARD": 2}

        try:
            opts, args = getopt.getopt(argv, "hi:l:w:", ["infile=", "level=", "words="])
        except getopt.GetoptError:
            return

        for opt, arg in opts:
            if opt == "-h":
                print(
                    "options -l <level> (0,1,2 or EASY,MEDIUM,HARD) -i <input_file> / -w <word_list>"
                )
                return

            elif opt in ("-l", "--level"):
                print(f"Level set to {arg}")
                if arg in level_conv_dict:
                    self._level_int = level_conv_dict[arg]
                elif arg in (0, 1, 2):
                    self._level_int = arg

            elif opt in ("-i", "--infile"):
                print(f"Input file set to {arg}")
                self._input_file = arg

            elif opt in ("-w", "--words"):
                print(f"Word list set to {arg}")
                self._word_list = arg

    @property
    def level(self):
        return self._level_int

    @property
    def input_file(self):
        return self._input_file

    @property
    def word_list(self):
        return self._word_list
