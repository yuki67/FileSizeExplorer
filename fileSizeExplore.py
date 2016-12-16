# -*- coding: utf-8 -*-
import os

import sys
import loggingUtility as lgu
import logging
import shelve
from folderInfo import FolderInfo


class FileSizeExplore():

    def __init__(self, dir):
        lgu.init()
        self.lookingAt = ''

        try:
            self.folderInfo = shelve.open(
                '.\\savedShelve\\fileSizeExplore')[dir]
            print('Successfully opened shelve of ' + dir)
        except KeyError:
            print('shelve file for ' + dir +
                  ' doesn\'t exist.\nDo you wont to make new one? [y/n]')
            response = input()
            if response == 'y':
                print('Making file size index. This may take some time...')
                self.folderInfo = FolderInfo(dir)
                print('Completed')
            else:
                print('exiting...')
                sys.exit()

        self.showInfo()

        response = input('Do you want to save the result?\n')
        if response == 'y':
            self.folderInfo.save(dir)
            print('Results saved.')
        else:
            print('exiting...')

    def showInfo(self):
        self.folderInfo.show()
        while(True):
            key = input('press q to exist.\n')
            if key == 'q':
                break
            else:
                self.lookingAt = self.connectPath(self.lookingAt, key)
                logging.debug('now looking at ' + self.lookingAt)
                try:
                    self.folderInfo.find(self.lookingAt).show()
                except KeyError:
                    print(os.path.join(self.folderInfo.name,
                                       self.lookingAt) + ' doesn\'t exist.')
                    self.lookingAt = self.lookingAt[:-len(key)]
                    logging.debug(
                        'that was wrong. now looking at ' + self.lookingAt)
                    self.folderInfo.find(self.lookingAt).show()
        print('done')

    def connectPath(self, cwd, dir):
        for name in dir.split('\\'):
            if name == '.':
                pass
            elif name == '..':
                cwd = os.path.split(cwd)[0]
            else:
                cwd = os.path.join(cwd, name)
        return cwd

FileSizeExplore('C:\\')
