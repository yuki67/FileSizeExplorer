# -*- coding: utf-8 -*-

import os


class FolderInfo():

    def __init__(self, directory):
        self.size = 0
        self.size_files = 0
        self.name = directory
        self.sub_dirs = {}
        try:
            for content in os.listdir(self.name):
                content = self.name + ".\\" + content
                if os.path.isfile(content):
                    # contentがファイルのとき
                    self.size += os.path.getsize(content)
                    self.size_files += os.path.getsize(content)
                else:
                    # contentがフォルダのとき
                    basename = os.path.basename(content)
                    self.sub_dirs[basename] = FolderInfo(content)
                    self.size += self.sub_dirs[basename].size
        except PermissionError:
            print('Failed to open : ' + self.name)
        except FileNotFoundError:
            print('Failed to open : ' + self.name)
        except NotADirectoryError:
            print('This file doesn\'t exist : ' + self.name)
