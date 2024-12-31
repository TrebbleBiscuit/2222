# 2222

An incredibly overengineered python implementation of 2222

**Features**
- Play in `Manual Advance` mode or `Fixed Time Per Word`
- See how many words you've done and how many are left
- Random word order
- Auto-download words
- Gracefully exit on `KeyboardInterrupt`

**`Manual Advance` Mode Features**
- Press enter to advance to next word
- Type `n` before hitting enter to record a mistake


### Optional Dependency

`pip install pyfiglet` for rendering ASCII art fonts - https://github.com/pwaller/pyfiglet/


### Usage

- Download and install python
- Download `two.py`
- `python two.py`

> [!NOTE]  
> This will automatically download `2222.txt` from the `2222` GitHub repo, placing it in the same directory as `two.py`


Change configuration options like this

```python
from two import GameMode, twotwotwotwo

twotwotwotwo(game_mode=GameMode.MANUAL_ADVANCE, random_order=True)
twotwotwotwo(game_mode=GameMode.FIXED_TIME_PER_WORD, random_order=False)
```

