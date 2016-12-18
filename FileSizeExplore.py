# -*- coding: utf-8 -*-
"""
FolderInfoの内容を表示
"""
import os
import argparse
import shelve
from FolderInfo import FolderInfo


class FileSizeExplorer():
    """
    フォルダーの要素のサイズを保持する。
    """

    def __init__(self):
        self.first_cwd = os.getcwd()
        self.args = self.make_perser().parse_args()
        self.cwd = self.clear_path(self.args.path)
        self.info = None
        if os.path.exists(self.cwd):
            self.prologue()
            self.loop()
            self.epilogue()
        else:
            print(self.cwd + "does not exist.")

    @staticmethod
    def shelve_exists(key, shelve_path):
        """
        pathにsavedShelveがあり、かつその中にkeyというkeyがあるかどうかを返す
        """
        if os.path.exists(shelve_path + ".\\savedShelve.dat"):
            slv = shelve.open(shelve_path + ".\\savedShelve")
            ans = key in slv.keys()
            slv.close()
            return ans
        else:
            return False

    def load_shelve(self, key):
        """
        savedShelveからkeyを読みだし、selfに代入する
        """
        slv = shelve.open("savedShelve")
        self.info = slv[key]
        slv.close()
        return

    def save_shelve(self, directory):
        """
        あとから読み出せるようにshelveに保存する。
       保存先はdirectory\\saved_shelve
        """
        slv = shelve.open(directory + "\\savedShelve")
        slv[self.info.name] = self.info
        slv.close()

    @staticmethod
    def make_perser():
        """
        パーサーを作って、パーサーを返す。
        返り値に直接parse_arg()することが前提になっている。
        """
        parser = argparse.ArgumentParser(description="Show folder size.")
        parser.add_argument("-p", dest="path", default=".//", required=False,
                            action="store", help="Configure folder path. " +
                            "Default : \".\\\"")
        return parser

    @staticmethod
    def clear_path(path):
        """
        pathを完全なパス(曖昧さのないパス)にして返す。
        """
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        return os.path.abspath(path)

    def prologue(self):
        """
        開始時のプロンプト。
        """
        print("target folder : " + self.cwd)
        while True:
            if self.shelve_exists(self.cwd, os.getcwd()):
                response = input(
                    "Saved shelve found. Road this shelve? [y/n] : ")
                if response == "y":
                    print("loading...")
                    self.load_shelve(self.cwd)
                    return
                elif response == "n":
                    break
            else:
                print("No saved shelve found.")
                break
        print("Collectiong imformation about %s."
              " This may take some time." % self.cwd)
        self.info = FolderInfo(self.cwd)
        print("You can reduce errors by running script as administrater.")

    def epilogue(self):
        """
        終了時のプロンプト。
        """
        while True:
            response = input("Do you want to save the result?[y/n] : ")
            if response == "y":
                self.save_shelve(self.first_cwd)
                print("Results saved.")
                break
            elif response == "n":
                print("exiting...")
                break

    def show(self, path):
        """
        pathフォルダの情報(そのフォルダのサイズとサブフォルダのサイズ)を返す。
        """
        temp_size = self.info.size
        temp_size_files = self.info.size_files
        temp_sub_dirs = self.info.sub_dirs
        rel_path = path.replace(self.info.name, "")
        # rel_path == ""のときpath = self.name
        if rel_path != "":
            if rel_path[0] == "\\":
                rel_path = rel_path[1:]
            for path in rel_path.split("\\"):
                temp_size = temp_sub_dirs[path].size
                temp_size_files = temp_sub_dirs[path].size_files
                temp_sub_dirs = temp_sub_dirs[path].sub_dirs

        result = {}
        result[temp_size_files] = "Files in this directory"
        for sub_dir in temp_sub_dirs.values():
            result[sub_dir.size] = "\\" + os.path.basename(sub_dir.name)

        return result, temp_size

    def show_info(self):
        """
        self.infoとself.cwdに基づいてフォルダの内容を表示する。
        """
        result, total_size = self.show(self.cwd)
        print("----- Contents of " + self.cwd + "-----")
        print("Total size : " + str(round(total_size / 1024 ** 2, 2)) + "MB")
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
            key = input("press q to exist.\n")
            if key == "q":
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
        print("done")

FileSizeExplorer()
