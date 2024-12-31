import logging
import random
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from urllib.request import urlopen

# hacky magic to make this dependency optional
try:
    import pyfiglet  # for pretty ascii art text
except ModuleNotFoundError:
    print(
        "WARNING: Module pyfiglet not found! 2222 words will look nicer if you `pip install pyfiglet`."
    )
    USE_FIGLET = False
else:
    USE_FIGLET = True

# The file that contains 2222 words
DEFAULT_WORDS_FILE_PATH = Path(__file__).parent / "2222.txt"

# Exactly how much time to spend on each word
# so that the whole thing takes 22:22 (1342 seconds)
TIME_PER_WORD = 1342 / 2222

# Auto-download words for ultra portability
GITHUB_WORDS_URL = (
    "https://raw.githubusercontent.com/ivanreese/2222/refs/heads/2222/2222.txt"
)


class GameMode(Enum):
    FIXED_TIME_PER_WORD = "Fixed Time"  # Each word visible for the same amount of time
    MANUAL_ADVANCE = "Manual Advance"  # Press enter to continue to the next word


def clear_screen():
    """Clear the screen and position the cursor at the top left."""
    escape_character = "\033"
    clear_screen = "[2J"
    move_cursor_to_top_left = "[1;1H"
    print(
        f"{escape_character}{clear_screen}{escape_character}{move_cursor_to_top_left}",
        end="",
    )


def get_2222_words(path_to_words_file: Path = DEFAULT_WORDS_FILE_PATH) -> list[str]:
    """Read 2222 words from a file, or download them from github.

    Args:
        path_to_words_file (Path, optional): Path to file containing exactly 2222 words. Defaults to DEFAULT_WORDS_FILE_PATH.

    Returns:
        list[str]: A list of 2222 words
    """
    # let's see if the file already exists
    if path_to_words_file.exists():
        with path_to_words_file.open("r") as txtfile:
            all_words = txtfile.readlines()
        # ensure it's 2222 words
        assert len(all_words) == 2222
        return all_words

    print(
        f"{path_to_words_file.name} does not exist! Downloading from {GITHUB_WORDS_URL}"
    )

    try:
        with urlopen(GITHUB_WORDS_URL) as response:
            content = response.read().decode("utf-8")
    except Exception as exc:
        raise Exception(
            f"Didn't find words on disk and failed to download from {GITHUB_WORDS_URL}",
        ) from exc
    else:
        print("Finished downloading 2222 words!")

    # Write these words to file so we can re-use them for next time
    with path_to_words_file.open("w") as words_file:
        words_file.write(content)

    return content.split("\n")


def print_header(
    game_mode: GameMode, start_time: datetime, recorded_mistakes: int, word_index: int
):
    """Print some pretty info above and before the actual word to read.

    Args:
        game_mode (GameMode): Game mode we're playing
        start_time (datetime): Time we started playing
        recorded_mistakes (int): Number of recorded mistakes so far
        word_index (int): Index of the word we're on
    """
    print(f"{word_index + 1}/2222")
    if recorded_mistakes:
        print(
            f"{recorded_mistakes} mistake{'s' if recorded_mistakes != 1 else ''} so far"
        )
    if game_mode == GameMode.MANUAL_ADVANCE:
        if word_index <= 5:
            print("\n")
            return
        seconds_elapsed = (datetime.now() - start_time).total_seconds()
        avg_sec_per_word = round(seconds_elapsed / (word_index + 1), 3)
        print(f"Avg seconds per word: {avg_sec_per_word}")

        if word_index <= 20:
            print("")
            return
        eta_sec = avg_sec_per_word * (2222 - word_index)
        if eta_sec > 60:
            print(f"about ~{round(eta_sec / 60)} minutes to go")
        else:
            print("ETA: <1m")


def print_word(word):
    if USE_FIGLET:
        print(pyfiglet.figlet_format(word, font="standard"))
    else:
        print("\n" + word)


def twotwotwotwo(
    game_mode: GameMode = GameMode.MANUAL_ADVANCE,
    random_order: bool = True,
):
    """Play a game of 2222.

    Args:
        game_mode (GameMode, optional): Which game mode to play. Defaults to GameMode.MANUAL_ADVANCE.
        random_order (bool, optional): Whether to randomize word order. Defaults to True.
    """
    # Read in 2222 words
    all_words = get_2222_words()

    # Randomize word order for extra spice
    if random_order:
        random.shuffle(all_words)

    print(f"Playing 2222 in {game_mode.value} mode")
    input("Press Enter to begin...")

    start_time = datetime.now()
    recorded_mistakes = 0
    i = 0

    # Iterate over words and show them on screen
    try:
        for i, word in enumerate(all_words):
            clear_screen()
            print_header(game_mode, start_time, recorded_mistakes, i)
            print_word(word)
            # figure out how to proceed to the next word
            if game_mode == GameMode.FIXED_TIME_PER_WORD:
                time.sleep(TIME_PER_WORD)
            elif game_mode == GameMode.MANUAL_ADVANCE:
                if "n" in input():
                    recorded_mistakes += 1
    except KeyboardInterrupt as exc:
        if i == 0:
            raise exc
    seconds_elapsed = (datetime.now() - start_time).total_seconds()
    print(f"Made it to word {i+1}/2222 in {round(seconds_elapsed)} seconds")
    if game_mode == GameMode.MANUAL_ADVANCE:
        print(f"{round(seconds_elapsed / i, 3)} seconds per word")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    twotwotwotwo(game_mode=GameMode.MANUAL_ADVANCE)
