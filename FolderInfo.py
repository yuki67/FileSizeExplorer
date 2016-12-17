# -*- coding: utf-8 -*-
"""
フォルダーの要素のサイズを保持する。
"""

import os
import shelve


class FolderInfo():
    """
    フォルダーについての情報を保持する。
    """

    def __init__(self, directory):
        self.size = 0
        self.size_files = 0
        self.name = os.path.abspath(directory)
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
                pass
                # print('Failed to open : ' + content)
            except NotADirectoryError:
                pass
                # print('This files doesn\'t seem to exist : ' + content)

    @staticmethod
    def shelve_exists(name):
        """
        savedShelveの中にnameというkeyがあるかどうかを返す
        """
        if os.path.exists("savedShelve.dat"):
            slv = shelve.open('savedShelve')
            ans = name in slv.keys()
            slv.close()
            return ans
        else:
            return False

    def copy(self, src):
        """
        srcの内容をselfにコピーする。
        """
        self.size = src.size
        self.size_files = src.size_files
        self.name = src.name
        self.sub_dirs = src.sub_dirs
        return self

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
        folderInfoをshelveに保存する。
        ディレクトリは.saved_shelve
        """
        slv = shelve.open(directory + "\\savedShelve")
        slv[self.name] = self
        slv.close()

    @staticmethod
    def percentage(total, size, digits=2):
        """
        selfのサイズに対するsizeの割合を返す。
        """
        return round(size / total * 100, digits)

    def show(self, abs_path):
        """
        abs_pathフォルダの情報を表示する。
        """
        temp_size = self.size
        temp_size_files = self.size_files
        temp_sub_dirs = self.sub_dirs
        rel_path = abs_path.replace(self.name, "")
        # rel_path == ""のときabs_path = self.name
        if rel_path != "":
            for path in rel_path.split("\\"):
                temp_size = temp_sub_dirs[path].size
                temp_size_files = temp_sub_dirs[path].size_files
                temp_sub_dirs = temp_sub_dirs[path].sub_dirs

        result = {}
        result[temp_size_files] = "Files in this directory"
        for sub_dir in temp_sub_dirs.values():
            result[sub_dir.size] = sub_dir.name

        print('----- Contents of ' + abs_path + '-----')
        print('Total size : ' + str(round(temp_size / 1024 ** 2, 2)) + 'MB')
        for size, name in sorted(result.items(), reverse=True):
            print(str(self.percentage(temp_size, size)).rjust(5) + '% ' +
                  str(round(size / 1024 ** 2, 2)).rjust(15) + "MB " + name.replace(self.name, "").rjust(25))
