# -*- coding: utf-8 -*-

import os
import sys
import logging
import shelve


class FolderInfo():

    def __init__(self, dir):
        self.size = 0
        self.name = os.path.abspath(dir)
        self.filesSize = 0
        self.folders = {}
        self.search(dir)

    def search(self, dir):
        try:
            for content in os.listdir(self.name):
                content = os.path.join(dir, content)
                # logging.debug('checking content ' + content)
                if os.path.isfile(content):
                    # logging.debug(content + ' is a file with size ' + str(os.path.getsize(content)))
                    self.size += os.path.getsize(content)
                    self.filesSize += os.path.getsize(content)
                else:
                    # logging.debug(content + ' is a folder')
                    newFolder = FolderInfo(content)
                    self.folders[os.path.basename(content)] = newFolder
                    self.size += newFolder.size
        except PermissionError:
            logging.debug('Failed to open : ' + dir)
        except NotADirectoryError:
            logging.debug('This files doesn\'t seem to exist : ' + dir)
        # logging.debug('Indexing ended : ' + name)

    def find(self, relPath):
        if relPath == '':
            return self
        paths = relPath.split('\\')
        ans = self
        for path in paths:
            ans = ans.folders[path]
        return ans

    def save(self, dir):
        os.makedirs('savedShelve', exist_ok=True)
        shelveFile = shelve.open('.\\savedShelve\\fileSizeExplore')
        shelveFile[dir] = self
        shelveFile.close()

    def percentage(self, size, digits=2):
        return round(size / self.size * 100, 2)

    def show(self):
        print('----- Contents of ' + self.name + '-----')
        print('Total size : ' + str(round(self.size / 1024 ** 2, 2)) + 'MB')
        for folder in self.folders.values():
            print(str(self.percentage(folder.size)).rjust(5) + '% ' +
                  str(round(folder.size / 1024 ** 2, 2)).rjust(12) + "MB"
                  " " + os.path.basename(folder.name))
        print(str(self.percentage(self.filesSize)).rjust(5) + '% ' +
              str(round(self.filesSize / 1024 ** 2)).rjust(12) + "MB "
              ' Files in this directory')
