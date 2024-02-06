'''
(crontab -l 2>/dev/null | echo "@reboot touch /home/test/Desktop/test.txt") | crontab -
'''

import os

class Cronjob:
    def __init__(self, payload):
        self.payload = payload

    