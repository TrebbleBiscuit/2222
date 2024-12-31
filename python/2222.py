import pyfiglet
import time
from pathlib import Path
import random

# path to the file which contains 2222 words
PATH_TO_WORDS = Path(__file__).parents[1] / "2222.txt"

# exactly how much time to spend on each word so that the whole thing takes 22:22
TIME_PER_WORD = 1342 / 2222


def clear_screen():
    escape_character = "\033"
    clear_screen = "[2J"
    move_cursor_to_top_left = "[1;1H"
    print(
        f"{escape_character}{clear_screen}{escape_character}{move_cursor_to_top_left}",
        end="",
    )


def twotwotwotwo(random_order: bool = True):
    # Read in 2222 words
    with PATH_TO_WORDS.open("r") as txtfile:
        all_words = txtfile.readlines()
    assert len(all_words) == 2222

    # Randomize word order for extra spice
    if random_order:
        random.shuffle(all_words)

    # Iterate over words and show them on screen
    for i, word in enumerate(all_words):
        clear_screen()
        print(f"{i}/{len(all_words)}")
        print(pyfiglet.figlet_format(word, font="standard"))
        time.sleep(TIME_PER_WORD)


if __name__ == "__main__":
    twotwotwotwo()
