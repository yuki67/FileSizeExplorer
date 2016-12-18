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
        self.cwd = self.clear_path(self.args.name)
        print(self.cwd)
        self.info = FolderInfo(self.cwd)
        self.loop()

    @staticmethod
    def make_perser():
        """
        パーサーを作って、パーサーを返す。
        返り値に直接parse_arg()することが前提になっている。
        """
        parser = argparse.ArgumentParser(description="Show folder size.")
        parser.add_argument("-n", dest="name", default=".//", required=False,
                            action="store", help="Configure folder name. " +
                            "Default : \".\\\"")
        return parser

    @staticmethod
    def clear_path(path):
        """
        pathを完全なパス(曖昧さのないパス)にして返す
        """
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        return os.path.abspath(path)

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

    def show_info(self):
        """
        self.infoとself.cwdに基づいてフォルダの内容を表示する。
        """
        result, total_size = self.info.show(self.cwd)
        print('----- Contents of ' + self.cwd + '-----')
        print('Total size : ' + str(round(total_size / 1024 ** 2, 2)) + 'MB')
        for size, name in sorted(result.items(), reverse=True):
            print("%5.2f%% %10.2fMB %s" %
                  (size / total_size * 100, size / 1048576, name))

    def loop(self):
        """
        メインループ
        """
        os.chdir(self.cwd)
        self.show_info()
        while True:
            key = input('press q to exist.\n')
            if key == 'q':
                break
            key = self.clear_path(key)
            if os.path.exists(key):
                if self.info.name in key:
                    self.cwd = key
                    os.chdir(self.cwd)
                else:
                    print("Information about " + key + " does not exist.")
            else:
                print("Path " + key + " does not exist.")
            self.show_info()
        print('done')
        self.epilogue()

FileSizeExplorer()
