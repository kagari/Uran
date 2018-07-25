# reader.py
# read file system
import os,sys
import curses

args = sys.argv

def readfile():
    with open(args[1]) as fi:
        s = fi.readlines()
        print(fi)
        # <class '_io.TextIOWrapper'>
        return s

def main(stdscr):
    # Clear screen
    file = readfile()
    stdscr.clear()
    for line in file:
#        stdscr.addstr(str(line))
    stdscr.getkey()
    

curses.wrapper(main)
