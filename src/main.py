import curses
import curses.ascii

def main(stdscr):
    stdscr.clear()
    while True:
        key = stdscr.getch() # 入力された文字の取得
        now_y, now_x = stdscr.getyx() # 現在のカーソル位置
        max_y, max_x = stdscr.getmaxyx() # ウィンドウの最大値取得
        # 文字を表示できる場所はウィンドウの最大に-1した場所まで
        max_y -= 1
        max_x -= 1
        # C-Xで終了
        if key == curses.ascii.CAN:
            break
        elif key in (curses.ascii.BS, curses.KEY_BACKSPACE):
            if now_x > 0:
                stdscr.delch(now_y, now_x-1) # 今のカーソルの一つ前の文字を削除

        # 右十字キー
        elif key == curses.KEY_RIGHT:
            if now_x < max_x:
                stdscr.move(now_y, now_x+1)

        elif key == curses.KEY_LEFT:
            if now_x > 0:
                stdscr.move(now_y, now_x-1)

        elif key == curses.KEY_DOWN:
            if now_y < max_y:
                stdscr.move(now_y+1, now_x)

        elif key == curses.KEY_UP:
            if now_y > 0:
                stdscr.move(now_y-1, now_x)

        # 他のキー、普通の文字など
        else:
            # 一番右下(max_y, max_x)でのaddchはカーソルが範囲外に行きエラーとなる(max_y+1, 0に移動でエラー)
            # そのため、現在カーソルが一番右下の場合は無視
            if now_x == max_x and now_y == max_y:
                pass
            elif now_y == max_y and key in (curses.KEY_ENTER, 10):
                pass
            else:
                stdscr.addch(key)
        stdscr.refresh()

curses.wrapper(main)
