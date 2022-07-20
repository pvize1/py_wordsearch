"""
Front-end for the word search app
"""

from wordsearch.helpers.word_list import WordList
from wordsearch.helpers.word_grid import WordGrid
import argparse
import wordsearch.words_list as wl


def check_infile(infile):
    print(f"Source: Input file={infile}")
    try:
        in_file = open(infile, "r")
        return in_file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"The input file '{infile}' not found")


def check_wordlist(wordlist):
    if wordlist in wl.word_list_dict:
        print(f"Source: Word list={wordlist}")
        return wl.word_list_dict[wordlist]
    else:
        raise TypeError("Word list not word_list dictionary")


def gen_word_list(list_of_words):
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


def handle_args():
    parser = argparse.ArgumentParser(
        description="Create wordsearch grid from list of words"
    )
    parser.add_argument(
        "-l",
        "--level",
        action="store",
        choices={0, 1, 2},
        type=int,
        default=0,
        help="difficulty level 0=easy, 3=hard",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-w", "--words", dest="words", help="Key of list in word_list.py"
    )
    group.add_argument(
        "-i", "--infile", dest="infile", help="Name of file with word list"
    )
    args = parser.parse_args()

    if args.words:
        raw_word_list = check_wordlist(args.words)
    elif args.infile:
        raw_word_list = check_infile(args.infile)
    else:
        raise SyntaxError("No list of words provided on command line")

    return args.level, gen_word_list(raw_word_list)


def main():
    # Return values: 0=Success, 1=File not found, 2=No valid clean words found
    level, word_iter = handle_args()
    new_list = WordList(word_iter)
    new_grid = WordGrid(level=level)

    if new_list.return_code == 0:
        new_grid.create_grid_and_place_words(new_list)
        print("\n")
        print("Words not placed: ")
        for wd_data in new_list:
            if not wd_data.placed:
                print(wd_data.word, wd_data.length)

        print("\n")
        print(f"Count of words: {new_list.word_count}")
        print(f"Longest word: {new_list.len_longest_word}  ({new_list.longest_word})")
        print(f"Grid size: {len(new_grid.word_grid)}")

        print("\n")
        for line in new_grid.word_grid:
            print(line)

        print("\n")
        print("Words placed: ")
        for wd_data in new_list:
            if wd_data.placed:
                print(wd_data.word, wd_data.line)
    else:
        return new_list.return_code


if __name__ == "__main__":
    main()
