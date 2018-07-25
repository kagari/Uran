import sys,os
import curses
from curses import textpad

def file_print(filename):
    fin = open(filename)
    str = 10
    if not fin:
        print("[error]can't open")
        return
    while True:
        line = fin.readline(str)
        if not line:
            break
        print(line)
    fin.close()

def main(stdscr):
    stdscr.clear() # 画面をクリア
    init() # 変数などの初期値を設定
    cursor_y, cursor_x = stdscr.getyx() # 現在のカーソル位置を取得
    # 編集を行う
    while True:
        key = stdscr.getch() # 入力待ち
        if not key: # 入力がNULLだった場合
            continue
        if not do_command(key): # do_commandに操作がなければ終了
            break
    # 終了前に画面をリフレッシュ
    stdscr.refresh() # 画面をリフレッシュ

def _update_max_yx():
    maxy, maxx = win.getmaxyx()
    maxy = maxy - 1
    maxx = maxx - 1

def _end_of_line(y): # 今いる行の最後の位置を返す
    "行の最大値から長さを一つずつ減らしていき、文字がある位置を探す"
    _update_max_yx()
    last = maxx
    while True:
        if curses.ascii.ascii(win.inch(y, last)) != curses.ascii.SP:
            last = min(maxx, last+1)
            break
        elif last == 0:
            break
        last = last - 1
    return last

def _insert_printabale_char(ch):
    _update_max_yx()
    (y, x) = win.getyx()
    backyx = None
    while y < maxy or x < maxx:
        if insert_mode:
            oldch = win.inch()
        try:
            win.addch(ch)
        except curses.error:
            pass
        if not insert_mode or not curses.ascii.isprint(oldch):
            break
        ch = oldch
        (y, x) = win.getyx()
        # Remember where to put the cursor back since we are in insert_mode
        if backyx is None:
            backyx = y, x

    if backyx is not None:
        win.move(*backyx)

def do_command(key):
    "Process a single editing command."
    _update_max_yx()
    (y, x) = win.getyx()
    lastcmd = ch
    if curses.ascii.isprint(ch):
        if y < maxy or x < maxx:
            _insert_printable_char(ch)
        elif ch == curses.ascii.SOH:                           # ^a
            win.move(y, 0)
        elif ch in (curses.ascii.STX,curses.KEY_LEFT, curses.ascii.BS,curses.KEY_BACKSPACE):
            if x > 0:
                win.move(y, x-1)
            elif y == 0:
                pass
            elif stripspaces:
                win.move(y-1, _end_of_line(y-1))
            else:
                win.move(y-1, maxx)
            if ch in (curses.ascii.BS, curses.KEY_BACKSPACE):
                win.delch()
        elif ch == curses.ascii.EOT:                           # ^d
            win.delch()
        elif ch == curses.ascii.ENQ:                           # ^e
            if stripspaces:
                win.move(y, _end_of_line(y))
            else:
                win.move(y, maxx)
        elif ch in (curses.ascii.ACK, curses.KEY_RIGHT):       # ^f
            if x < maxx:
                win.move(y, x+1)
            elif y == maxy:
                pass
            else:
                win.move(y+1, 0)
        elif ch == curses.ascii.BEL:                           # ^g
            return 0
        elif ch == curses.ascii.NL:                            # ^j
            if maxy == 0:
                return 0
            elif y < maxy:
                win.move(y+1, 0)
        elif ch == curses.ascii.VT:                            # ^k
            if x == 0 and _end_of_line(y) == 0:
                win.deleteln()
            else:
                # first undo the effect of _end_of_line
                win.move(y, x)
                win.clrtoeol()
        elif ch == curses.ascii.FF:                            # ^l
            win.refresh()
        elif ch in (curses.ascii.SO, curses.KEY_DOWN):         # ^n
            if y < maxy:
                win.move(y+1, x)
                if x > _end_of_line(y+1):
                    win.move(y+1, _end_of_line(y+1))
        elif ch == curses.ascii.SI:                            # ^o
            win.insertln()
        elif ch in (curses.ascii.DLE, curses.KEY_UP):          # ^p
            if y > 0:
                win.move(y-1, x)
                if x > _end_of_line(y-1):
                    win.move(y-1, _end_of_line(y-1))
        return 1

def edit():
    while True:
        ch = win.getch()
        if not ch:
            continue
        if not do_command(ch):
            break
        win.refresh()
    return gather()

if __name__ == '__main__':
    def test_editbox(stdscr):
        stdscr.clear()
        stdscr.addstr("Use q to end editing.")
        win = curses.newwin()
        stdscr.refresh()
        return Textbox(win).edit()

    str = curses.wrapper(test_editbox)
    print("Contents of text box:", repr(str))
