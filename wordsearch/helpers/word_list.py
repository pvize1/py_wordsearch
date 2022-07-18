"""
Word_List class manages list of clean words and placement
in the Word_Grid
"""

from collections import Counter
import wordsearch.words_list as wl
from pathlib import Path


class WordData:
    """ WordData class """

    def __init__(self, word):
        """
        """
        self._word = word
        self._length = len(word)
        self._start_x = 0
        self._start_y = 0
        self._direction = ""
        self._placed = False
        self._found = False
        self._letter_freq = Counter(word)

    def update_data(self, start_x, start_y, direction, placed=False, found=False):
        """
        """
        self._start_x = start_x
        self._start_y = start_y
        self._direction = direction
        self._placed = placed
        self._found = found

    @property
    def word(self):
        return self._word

    @property
    def length(self):
        return self._length

    @property
    def placed(self):
        return self._placed

    @property
    def freq_dict(self):
        return self._letter_freq

    @property
    def line(self):
        return f"Length={self._length}; Start X,Y={self._start_x}, {self._start_y}; Direction={self._direction}"


class WordList:
    """ WordList class """

    def __init__(self, passed_list=None, infile="", wordlist=""):
        """
        """
        self._word_data = []
        # TODO Set dictionary key=word to index self._word_data_dict = {}
        self._all_freq_data_dict = Counter()
        self._len_longest_word = 0
        self._longest_word = ""
        self._word_count = 0
        self._return_code = 0

        if wordlist:
            raw_word_list = self._check_wordlist(wordlist)
        elif infile:
            raw_word_list = self._check_infile(infile)
        else:
            raw_word_list = self._check_passed_list(passed_list)

        if len(raw_word_list) == 0:
            raise ValueError("Word list is empty")

        iter_words = self._gen_word_list(raw_word_list)
        for word in iter_words:
            wd_data = WordData(word)
            self._word_data.append(wd_data)
            self._all_freq_data_dict += wd_data.freq_dict

        self._word_count = len(self._word_data)
        if self._word_count > 0:
            self._word_data.sort(key=lambda wd: wd.length, reverse=True)
            self._longest_word = self._word_data[0].word
            self._len_longest_word = self._word_data[0].length
        else:
            raise ValueError("No valid clean words found")

    def __len__(self):
        return self._word_count

    def __getitem__(self, item):
        return self._word_data[item]

    def __iter__(self):
        print("WordList __iter__ called")
        return iter(self._word_data)

    @staticmethod
    def _gen_word_list(list_of_words):
        """
        Generator to go through list of words passed,
        Generator validates (greater than 2 chars and only alpha) and cleans (trim, upper) the words

        Args:
            list_of_words (list):

        Returns: Yields a cleaned and valid word
        """
        for word in list_of_words:
            clean_word = str(word).upper().strip()
            if len(clean_word) > 2 and str(clean_word).isalpha():
                yield clean_word

    @staticmethod
    def _check_infile(infile):
        print(f"Source: Input file={infile}")
        try:
            in_file = open(infile, "r")
            return in_file.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"The input file '{infile}' not found")

    @staticmethod
    def _check_passed_list(passed_list):
        if passed_list is None:
            return []
        if isinstance(passed_list, list):
            print(f"Source: Passed list")
            return passed_list
        else:
            raise TypeError("Passed list not a list")

    @staticmethod
    def _check_wordlist(wordlist):
        if wordlist in wl.word_list_dict:
            print(f"Source: Word list={wordlist}")
            return wl.word_list_dict[wordlist]
        else:
            raise TypeError("Word list not word_list dictionary")

    @property
    def letter_freq(self):
        return list(self._all_freq_data_dict.keys())

    @property
    def len_longest_word(self):
        return self._len_longest_word

    @property
    def longest_word(self):
        return self._longest_word

    @property
    def return_code(self):
        return self._return_code

    @property
    def word_count(self):
        return self._word_count
