"""
Word_Grid class manages matrix of letters hiding word list
Keeps list of words with flag for when word is found
Locates longest word to set matrix size (square=True)
Randomises words within matrix
Fills gaps with (optional) hidden message -> matrix size
"""

import random
import string
import numpy as np
from enum import IntEnum
from datetime import datetime


class WordGrid:
    """ WordGrid class """

    class DirectionInt(IntEnum):
        ACROSS = 0
        DOWN = 1
        DIAGONAL = 2

    direction_offset_dict = {
        DirectionInt.ACROSS: (1, 0),
        DirectionInt.DOWN: (0, 1),
        DirectionInt.DIAGONAL: (1, 1),
    }

    class LevelInt(IntEnum):
        EASY = 0
        MEDIUM = 1
        HARD = 2

    def __init__(self, level=LevelInt.EASY):
        """
        Args:
            level (IntEnum):
        """
        print("\ninit start=", datetime.now(tz=None))
        self._word_grid = np.full((1, 1), " ")
        self._level = self.LevelInt(level)
        print(f"Level = {self._level.name}")
        self._x, self._y = 0, 0

    def create_grid_and_place_words(self, word_list_obj):
        """
        Create an empty grid, then iterates through word list
        and places words in word grid

        Returns: None
        """
        print("create_grid_and_place_words start =", datetime.now(tz=None))
        grid_len = word_list_obj.len_longest_word + self._grid_pad_by_level(self._level)
        self._word_grid = np.resize(self._word_grid, (grid_len, grid_len))
        self._x, self._y = grid_len - 1, grid_len - 1
        direction_list = self._direction_list_by_level(self._level)

        # Only first word is placed totally randomly, as grid is empty
        direction = random.choice(direction_list)
        word_list_iter = iter(word_list_obj)
        wd_data = next(word_list_iter)
        x, y = self._get_random_vector(direction, wd_data.length, self._x, self._y)
        self._add_word(wd_data.word, x, y, direction)
        wd_data.update_data(x, y, direction.name, True)
        print("create_grid_and_place_words first =", datetime.now(tz=None))

        # otherwise list of available slots built
        for wd_data in word_list_iter:
            available_cells = list(
                zip(
                    *np.where(
                        (self._word_grid == " ") | (self._word_grid == wd_data.word[0])
                    )
                )
            )

            tries = 0
            direction = random.choice(direction_list)

            while tries < 3:
                slot_list = self._find_slots_in_direction(
                    wd_data.word, wd_data.length, direction, available_cells
                )
                if len(slot_list) > 0:
                    x, y, direction = random.choice(slot_list)
                    self._add_word(wd_data.word, x, y, direction)
                    wd_data.update_data(x, y, direction.name, True)
                    break
                else:
                    direction = self.DirectionInt(
                        (direction + 1) % (2 if self._level == 0 else 3)
                    )
                tries += 1

        print("create_grid_and_place_words rest =", datetime.now(tz=None))

        fill_letters = self._gen_filler(word_list_obj.letter_freq)
        blank_cells = list(zip(*np.where((self._word_grid == " "))))
        for x, y in blank_cells:
            pass
            self._word_grid[x, y] = random.choice(fill_letters)
        print("create_grid_and_place_words end =", datetime.now(tz=None))

    def _add_word(self, word, x: int, y: int, direction: DirectionInt):
        word_arr = list(word)
        if direction == self.DirectionInt.ACROSS:
            # TODO changing x is NOT across, but convention in rest of program
            length = len(word_arr) + x
            # print(f"ACROSS: x={x}, y={y}, length={length}")
            self._word_grid[x:length, y] = word_arr
        elif direction == self.DirectionInt.DOWN:
            # TODO changing y is NOT down, but convention in rest of program
            length = len(word_arr) + y
            # print(f"DOWN: x={x}, y={y}, length={length}")
            self._word_grid[x, y:length] = word_arr
        elif direction == self.DirectionInt.DIAGONAL:
            self._add_word_diag(word, x, y)

    def _add_word_diag(self, word, x, y):
        for letter in word:
            self._word_grid[x, y] = letter
            x += 1
            y += 1

    def _check_word_across(self, word, x, y):
        for letter in word[1:]:
            x += 1
            if self._not_check_cell(self._word_grid[x, y], letter):
                return False
        return True

    def _check_word_down(self, word, x, y):
        for letter in word[1:]:
            y += 1
            if self._not_check_cell(self._word_grid[x, y], letter):
                return False
        return True

    def _check_word_diag(self, word, x, y):
        for letter in word[1:]:
            x += 1
            y += 1
            if self._not_check_cell(self._word_grid[x, y], letter):
                return False
        return True

    def _find_slots_in_direction(
        self, word, word_len, direction: DirectionInt, cells
    ) -> list:
        """
         Returns a list of co-ordinates where the current word can fit,
         given the direction of travel

         Args:
             word (str): Word to search for
             word_len (int): Length of word
             direction (IntEnum): Direction of travel of searching for slots
             cells (list): List of tuples of (x,y) of suitable starting points

         Returns: List of available slots (x, y, direction)
         """
        if direction == self.DirectionInt.ACROSS:
            x_range = self._x - word_len
            return [
                (x, y, direction)
                for x, y in cells
                if ((x < x_range) and self._check_word_across(word, x, y))
            ]
        elif direction == self.DirectionInt.DOWN:
            y_range = self._y - word_len
            return [
                (x, y, direction)
                for x, y in cells
                if ((y < y_range) and self._check_word_down(word, x, y))
            ]
        else:
            x_range = self._x - word_len
            y_range = self._y - word_len
            return [
                (x, y, direction)
                for x, y in cells
                if ((x < x_range and y < y_range) and self._check_word_diag(word, x, y))
            ]

    def _get_random_vector(self, direction: DirectionInt, word_len, x, y) -> (int, int):
        """
        Returns a random integer to place word in a grid (row or column),
        but is aware of direction of word, so that e.g. whole row can be
        used if word travel is down

        Args:
            direction (IntEnum): direction of travel for word chosen
            word_len (int): Length of word


        Returns: tuple of x and y
        """
        if direction == self.DirectionInt.ACROSS:
            return random.randint(0, (x - word_len)), random.randint(0, y)
        elif direction == self.DirectionInt.DOWN:
            return random.randint(0, x), random.randint(0, (y - word_len))
        else:
            return (
                random.randint(0, (x - word_len)),
                random.randint(0, (y - word_len)),
            )

    def _direction_list_by_level(self, lvl: int) -> list:
        """
        Args:
            lvl (int): LevelInt enum passed as int to set level
            (0=Easy - 2=Hard)

        Returns: list of DirectionInt enum directions passed as int
        list is used to randomly set direction word will travel
        """
        if lvl == self.LevelInt.EASY:
            return [
                self.DirectionInt.ACROSS,
                self.DirectionInt.ACROSS,
                self.DirectionInt.DOWN,
            ]
        elif lvl == 1:
            return [
                self.DirectionInt.ACROSS,
                self.DirectionInt.ACROSS,
                self.DirectionInt.DOWN,
                self.DirectionInt.DOWN,
                self.DirectionInt.DOWN,
            ]
        else:
            return [
                self.DirectionInt.ACROSS,
                self.DirectionInt.DOWN,
                self.DirectionInt.DIAGONAL,
            ]

    @staticmethod
    def _gen_filler(list_of_letters):
        all_letters = list(string.ascii_uppercase)
        random.shuffle(all_letters)
        fill_list = list(list_of_letters)
        fill_list.extend(all_letters)
        return fill_list[0:12]

    @staticmethod
    def _grid_pad_by_level(lvl) -> int:
        if lvl == 0:
            return random.randint(2, 5)
        elif lvl == 1:
            return random.randint(4, 7)
        else:
            return random.randint(6, 9)

    @staticmethod
    def _not_check_cell(cell, letter):
        if cell == " ":
            return False
        else:
            if cell == letter:
                return False
            else:
                return True

    @property
    def word_grid(self):
        return self._word_grid
