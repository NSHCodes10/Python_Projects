import curses
from curses import wrapper
import time


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Type Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.clear()

    #split text into lines based on terminal width

    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, f"Height: {height}, Width: {width}")
    target_lines = []
    current_lines = []

    words =  target.split()
    current_word = ""

    #splitting target text into properly wrapped lines.
    for word in words:
        if len(current_word) + len(word) + 1 > width:
             target_lines.append(current_word)
             current_word = word
        else:
            if current_word:
                current_word += " " + word
            else:
                current_word = word
    target_lines.append(current_word)   #Append last line.

    current_text_str =  "".join(current)
    current_words = current_text_str.split()
    current_word = ""

    for word in current_words:
        if len(current_word) + len(word) + 1 > width:
            current_lines.append(current_word)
            current_word =  word
        else:
            if current_word:
                current_word += " " + word
            else:
                current_word = word
    current_lines.append(current_word)

    #Display the original text

    for i, line in enumerate(target_lines):
        stdscr.addstr(i, 0, line, curses.color_pair(3))   #Display each line of target text

    #Display user input

    for i, line in enumerate(current_lines):
        for j, char in enumerate(line):
            correct_char = target_lines[i][j] if i < len(target_lines) and j < len(target_lines[i]) else None
            color = curses.color_pair(1) if correct_char == char else curses.color_pair(2)
            stdscr.addstr(i + len(target_lines) + 1, j, char, color ) #move input below target text

    #display WPM counter at the bottom
    stdscr.addstr(len(target_lines) + len(current_lines) + 2, 0, f"WPM: {wpm}", curses.color_pair(3))

    #Move the cursor to where the next character should be typed

    if len (current_lines) > 0:
        stdscr.move(len(target_lines) + 1, len(current_lines[-1]))  #Move cursor to the end of user input
    else:
        stdscr.move(len(target_lines) + 1, 0)     #If no input, move cursor to the beginning

def load_text():
    with open("Curses_Module_SetUp2.txt", "r", encoding="utf-8") as f:
        return f.read().replace("\n", " ").strip()

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)     #Non blocking input

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text)/ 5) / (time_elapsed / 60))   #WPM formula

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # ESC key to exit
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if current_text:  # Prevent popping from empty list
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct input
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Incorrect input
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default text
    stdscr.clear()
    
    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(24, 0, "You completed the text! Press any key to continue...", curses.color_pair(3))
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)
