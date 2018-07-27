# reader.py
# read file system
import os,sys
import curses
import curses.ascii

def file_open(filename):
    with open(filename) as fin:
        if fin:
            s = fin.readlines()
            # <class '_io.TextIOWrapper'>
        else:
            s = "new file create"
        return s

def _update_max_yx():
    my, mx = stdscr.getmaxyx()
    my -= 1
    mx -= 1

def _end_of_line(y): #search end of line in cursor line
    last = mx
    while True:
        if curses.ascii.ascii(stdscr.inch(ny, last)) != curses.ascii.SP:
            last = min(mx, last+1)
            break
        elif last == 0:
            break
        last = last - 1
    return last

def main(stdscr):
    args = sys.argv
    file = file_open(args[1])
    my, mx = stdscr.getmaxyx()
    stline, enline = 0, my-1 # start and end line number
    while True:
        stdscr.clear() # Clear screen
        for i in file[stline:enline]:
            stdscr.addstr(i)
        key = stdscr.getch()
        ny, nx = stdscr.getyx()
        if key == ord('q'):
            break
        elif key in (curses.ascii.BS, curses.KEY_BACKSPACE):
            stdscr.delch(ny, nx-1)  # 今のカーソルの、一つ前の文字を削除
        elif key in (curses.ascii.SO, curses.KEY_DOWN):
            # 下矢印またはC-nを押した時に、表示できる最後の行だったらファイルの次の行を表示
            if ny < my-1:
                stdscr.move(ny+1, nx)
                if nx > _end_of_line(ny+1):
                    stdscr.move(ny+1, _end_of_line(ny+1))
            elif ny == my-1:
                if enline < len(file) - 1:
                    stline += 1
                    enline += 1
        elif key in (curses.ascii.DLE, curses.KEY_UP):
            if ny > 0:
                stdscr.move(ny-1, nx)
                #if nx > _end_of_line(ny-1):
                #     stdscr.move(ny-1, _end_of_line(ny-1))
            elif ny == 0:
                if stline > 0:
                    stline -= 1
                    enline -= 1
        elif key == curses.ascii.SI:
            stdscr.insertln()
        else:
            stdscr.addch(key)
    stdscr.refresh()
    return file

if __name__ == '__main__':
    str = curses.wrapper(main)
    #print(repr(str))
