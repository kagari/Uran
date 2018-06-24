import math
import sys
import time

END = 170
MAX_LEN = 30

def get_progressbar_str(progress):
    BAR_LEN = int(MAX_LEN * progress)
    return ('\x1b[1;32m[' + '=' * BAR_LEN +
            ('>' if BAR_LEN < MAX_LEN else '') +
            ' ' * (MAX_LEN - BAR_LEN) +
            '] %.1f%%\x1b[0m' % (progress * 100.))

sys.stderr.write('\r\033[2J\r\033[H') #clearDisplay
for i in range(END + 1):
    time.sleep(0.01)
    progress = 1.0 * i / END
    sys.stderr.write('\r\033[K' + get_progressbar_str(progress))
    sys.stderr.flush()
sys.stderr.write('\n')
sys.stderr.flush()
