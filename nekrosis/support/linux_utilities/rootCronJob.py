'''
(crontab -l 2>/dev/null | echo "@reboot touch /home/test/Desktop/test.txt") | crontab -
'''

import os


