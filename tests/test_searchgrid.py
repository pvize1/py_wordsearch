"""
xTODO: 1) Accept List of words, and store cleaned (upper, trim)
xTODO: 2) Validate list (all alpha only words, >2 chars) and count elements
xTODO: 3) Get longest word
xTODO: 4) Create empty matrix (x & y = longest word len) with 0-4 padding
xTODO: 5) Place word at position 0,0
xTODO: 6) Add direction flag to place word, create ENUM for A=Across, D=Down
xTODO: 7) Add Diagonal direction
xTODO: 8) Calculate letter freq using Counter
xTODO: 9) Fill grid with random letters (using letter freq)
xTODO: 10) Add level (complexity) to init (include diag direction)
xTODO: 11) Record where word placed: x,y,direction,Found Flag and return as property
xTODO: 12) Strategy to place words (with overlap)
TODO: 15) Add ability to set matrix size, square or not
"""

import pytest
from wordsearch.helpers.word_list import WordList
from wordsearch.helpers.word_grid import WordGrid
from wordsearch.runner import gen_word_list


def test_list_of_words_cleaned():
    """ Pass list of words and test that stored and cleaned """
    test_list = WordList(gen_word_list([" NewWord ", "memenTO   ", "One", "Two", "Three"]))
    assert test_list[0].word == "NEWWORD"
    assert test_list[1].word == "MEMENTO"


def test_list_of_words_valid():
    """ Pass list of words and test that invalid not stored """
    with pytest.raises(ValueError):
        test_list = WordList(gen_word_list([" word21 ", "memen TO  ", "be"]))


def test_clean_word_count():
    """ Pass list of words and test that stored and cleaned """
    test_list = WordList(gen_word_list([" NewWord ", "memenTO   ", "be", "word21", "Peter"]))
    assert test_list.word_count == 3


def test_longest_clean_word():
    """ Pass list of words and test that stored and cleaned """
    test_list = WordList(gen_word_list([" NeWord ", "menTO   ", "be", "wor21", "PeterVize", "thre"]))
    assert test_list.len_longest_word == 9


def test_create_grid():
    test_list = WordList(gen_word_list(["One", "Two", "Three"]))
    test_grid = WordGrid()
    test_grid.create_grid_and_place_words(test_list)
    assert len(test_grid.word_grid) >= 5


def test_fill_grid_lvl_one():
    test_list = WordList(gen_word_list(["One", "Two", "Three"]))
    test_grid = WordGrid()
    test_grid.create_grid_and_place_words(test_list)
    print("\n")
    print(test_grid.word_grid)
    for wd_data in test_list:
        assert wd_data.placed


def test_set_level_one():
    test_list = WordList(gen_word_list(["One", "Two", "Three", "Four"]))
    test_grid = WordGrid(level=1)
    test_grid.create_grid_and_place_words(test_list)
    print("\n")
    print(test_grid.word_grid)
    for wd_data in test_list:
        assert wd_data.placed


def test_set_level_two():
    test_list = WordList(gen_word_list(
        ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
    ))
    test_grid = WordGrid(level=2)
    test_grid.create_grid_and_place_words(test_list)
    print("\n")
    print(test_grid.word_grid)
    for wd_data in test_list:
        print(wd_data.word, wd_data.line)
        assert wd_data.placed
