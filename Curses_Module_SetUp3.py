import curses
from curses import wrapper
import time

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Type Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def load_text():
    with open("Curses_Module_SetUp3.txt", "r", encoding="utf-8") as f:
        return f.read().replace("\n", " ").strip()

def display_text(stdscr, target, current, wpm=0):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Display the text properly wrapped
    lines = []
    words = target.split()
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > width:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    lines.append(current_line)

    # User input management
    current_text_str = "".join(current)
    cursor_x, cursor_y = 0, 0
    
    # Display target text with colors
    for i, line in enumerate(lines):
        stdscr.addstr(i, 0, line, curses.color_pair(3))
        
    # Display user input
    for i, char in enumerate(current_text_str):
        row, col = divmod(i, width)
        if row < len(lines) and col < len(lines[row]):
            color = curses.color_pair(1) if char == lines[row][col] else curses.color_pair(2)
            stdscr.addstr(row, col, char, color)
            cursor_x, cursor_y = col + 1, row
    
    # Display WPM counter
    stdscr.addstr(len(lines) + 2, 0, f"WPM: {wpm}", curses.color_pair(3))
    
    # Move cursor to current position
    stdscr.move(cursor_y, cursor_x)

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)
    
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / 5) / (time_elapsed / 60))
        
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
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct input
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Incorrect input
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default text
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(24, 0, "You completed the text! Press any key to continue...", curses.color_pair(3))
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)