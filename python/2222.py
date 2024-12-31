import logging
import random
import time
from pathlib import Path
from urllib.request import urlopen
from enum import Enum
from datetime import datetime
import pyfiglet  # for pretty ascii art text

logger = logging.getLogger(__name__)

# The file that contains 2222 words
DEFAULT_WORDS_FILE_PATH = Path(__file__).parents[1] / "2222.txt"

# Exactly how much time to spend on each word
# so that the whole thing takes 22:22 (1342 seconds)
TIME_PER_WORD = 1342 / 2222

# Auto-download words for ultra portability
GITHUB_WORDS_URL = (
    "https://raw.githubusercontent.com/ivanreese/2222/refs/heads/2222/2222.txt"
)


def clear_screen():
    escape_character = "\033"
    clear_screen = "[2J"
    move_cursor_to_top_left = "[1;1H"
    print(
        f"{escape_character}{clear_screen}{escape_character}{move_cursor_to_top_left}",
        end="",
    )


def get_2222_words(path_to_words_file: Path = DEFAULT_WORDS_FILE_PATH):
    # let's see if the file already exists
    if path_to_words_file.exists():
        with path_to_words_file.open("r") as txtfile:
            all_words = txtfile.readlines()
        # ensure it's 2222 words
        assert len(all_words) == 2222
        return all_words

    logger.info(
        "%s does not exist! Downloading from %s", path_to_words_file, GITHUB_WORDS_URL
    )

    try:
        with urlopen(GITHUB_WORDS_URL) as response:
            content = response.read().decode("utf-8")
    except Exception as exc:
        raise Exception(
            f"Didn't find words on disk and failed to download from {GITHUB_WORDS_URL}",
        ) from exc

    # Write these words to file so we can re-use them for next time
    with path_to_words_file.open("w") as words_file:
        words_file.write(content)

    all_words = content.split("\n")


class GameMode(Enum):
    FIXED_TIME_PER_WORD = 0
    MANUAL_ADVANCE = 1


def twotwotwotwo(
    game_mode: GameMode = GameMode.MANUAL_ADVANCE,
    random_order: bool = True,
):
    # Read in 2222 words
    all_words = get_2222_words()

    # Randomize word order for extra spice
    if random_order:
        random.shuffle(all_words)

    logger.info("Playing 2222 in mode %s", game_mode)
    input("Press Enter to begin...")

    start_time = datetime.now()
    recorded_mistakes = 0

    # Iterate over words and show them on screen
    try:
        for i, word in enumerate(all_words):
            clear_screen()
            print(f"{i + 1}/{len(all_words)}")
            if recorded_mistakes:
                print(f"{recorded_mistakes} mistakes so far")
            if game_mode == GameMode.MANUAL_ADVANCE and i != 0:
                seconds_elapsed = (datetime.now() - start_time).total_seconds()
                avg_sec_per_word = round(seconds_elapsed / (i + 1), 2)
                print(f"Avg seconds per word: {avg_sec_per_word}")
                eta_sec = avg_sec_per_word * (2222 - i)
                if eta_sec > 60:
                    print(f"about ~{round(eta_sec / 60)} minutes to go")
                else:
                    print("ETA: <1m")
            print(pyfiglet.figlet_format(word, font="standard"))
            # figure out how to proceed to the next word
            if game_mode == GameMode.FIXED_TIME_PER_WORD:
                time.sleep(TIME_PER_WORD)
            elif game_mode == GameMode.MANUAL_ADVANCE:
                if "n" in input():
                    recorded_mistakes += 1
    except KeyboardInterrupt:
        print(i)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    twotwotwotwo()
