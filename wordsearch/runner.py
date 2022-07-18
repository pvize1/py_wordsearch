"""
Front-end for the word search app
"""


from wordsearch.helpers.handle_args import HandleArgs
from wordsearch.helpers.word_list import WordList
from wordsearch.helpers.word_grid import WordGrid
import sys


def main(argv):
    # Return values: 0=Success, 1=File not found, 2=No valid clean words found
    args = HandleArgs(argv)
    new_list = WordList(wordlist=args.word_list, infile=args.input_file)
    new_grid = WordGrid(level=args.level)

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
    main(sys.argv[1:])
