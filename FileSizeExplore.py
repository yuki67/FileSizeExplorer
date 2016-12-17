# -*- coding: utf-8 -*-
"""
FolderInfoの内容を表示
"""
import os
import argparse
from FolderInfo import FolderInfo


class FileSizeExplorer():
    """
    フォルダーの要素のサイズを保持する。
    """

    def __init__(self):
        self.first_cwd = os.getcwd()
        self.args = self.make_perser().parse_args()
        print(self.args)
        self.info = FolderInfo(os.path.abspath(self.args.name))
        self.cwd = os.path.abspath(self.args.name)
        os.chdir(self.cwd)
        self.loop()
        self.epilogue()

    def make_perser(self):
        parser = argparse.ArgumentParser(description="Show folder size.")
        parser.add_argument("-n", dest="name", default=".//", required=False,
                            action="store", help="Configure folder name. " +
                            "Default : \".\\\"")
        return parser

    def epilogue(self):
        """
        終了時のプロンプト。
        """
        response = input('Do you want to save the result?[y/n]:')
        if response == 'y':
            self.info.save_shelve(self.first_cwd)
            print('Results saved.')
        else:
            print('exiting...')

    def loop(self):
        """
        メインループ
        """
        self.info.show(self.cwd)
        while True:
            key = input('press q to exist.\n')
            if key == 'q':
                break
            if os.path.exists(key):
                if self.info.name <= os.path.abspath(key):
                    self.cwd = os.path.abspath(key)
                    os.chdir(self.cwd)
                else:
                    print("Information about " +
                          os.path.abspath(key) + " does not exist.")
            else:
                print("Path " + key + " does not exist.")
            self.info.show(self.cwd)
        print('done')

FileSizeExplorer()
