import sys

sys.stderr.write("\r\033[2J\r\033[H") # clear
sys.stderr.write("\r\033[31m\r\033[47m") # color
# argv.pyを実行するときに引数としたものを順番に返す
for i in range(len(sys.argv)):
    print("receive >",sys.argv[i])
