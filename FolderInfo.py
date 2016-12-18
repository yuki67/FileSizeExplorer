# -*- coding: utf-8 -*-
"""
フォルダーのサイズを保持する。
"""

import os
import shelve


class FolderInfo():
    """
    フォルダーについての情報を保持する。
    関数の引数が有効なパスかどうかを判定しない。
    """

    def __init__(self, directory):
        self.size = 0
        self.size_files = 0
        self.name = directory
        self.sub_dirs = {}
        self.construct()

    def construct(self):
        """
        フォルダの要素(=ファイルorフォルダ)をスキャンし、注目しているフォルダ(=self.name)のサイズを求める。
        """
        if self.shelve_exists(self.name):
            self.load_shelve(self.name)
        else:
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

    @staticmethod
    def shelve_exists(name):
        """
        cwdにsavedShelveがあり、かつその中にnameというkeyがあるかどうかを返す
        """
        if os.path.exists("savedShelve.dat"):
            slv = shelve.open('savedShelve')
            ans = name in slv.keys()
            slv.close()
            return ans
        else:
            return False

    def load_shelve(self, name):
        """
        savedShelveからnameを読みだし、selfに代入する
        """
        slv = shelve.open('savedShelve')
        self.size = slv[name].size
        self.size_files = slv[name].size_files
        self.name = slv[name].name
        self.sub_dirs = slv[name].sub_dirs
        slv.close()
        return self

    def save_shelve(self, directory):
        """
        あとから読み出せるようにshelveに保存する。
        ディレクトリはdirectory\\saved_shelve
        """
        slv = shelve.open(directory + "\\savedShelve")
        slv[self.name] = self
        slv.close()

    def show(self, path):
        """
        pathフォルダの情報(そのフォルダのサイズとサブフォルダのサイズ)を返す。
        """
        temp_size = self.size
        temp_size_files = self.size_files
        temp_sub_dirs = self.sub_dirs
        rel_path = path.replace(self.name, "")[1:]
        # rel_path == ""のときpath = self.name
        if rel_path != "":
            for path in rel_path.split("\\"):
                temp_size = temp_sub_dirs[path].size
                temp_size_files = temp_sub_dirs[path].size_files
                temp_sub_dirs = temp_sub_dirs[path].sub_dirs

        result = {}
        result[temp_size_files] = "Files in this directory"
        for sub_dir in temp_sub_dirs.values():
            result[sub_dir.size] = ".\\" + os.path.basename(sub_dir.name)

        return result, temp_size
