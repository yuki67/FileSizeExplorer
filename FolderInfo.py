# -*- coding: utf-8 -*-

import os


class FolderInfo():

    def __init__(self, path):
        self.path = path     # フォルダの絶対パス
        self.size = 0        # フォルダのサイズ
        self.size_files = 0  # フォルダにあるファイルのサイズの合計
        self.sub_dirs = {}   # フォルダにあるフォルダのFolderInfoを入れる
        try:
            for content in os.listdir(self.path):
                # この関数内ではcwdを変更しないので絶対パスに変換
                content = os.path.join(self.path, content)
                if os.path.islink(content):
                    # そのファイルそのものを指しているシンボリックリンクが(なぜか)たまにある
                    if os.path.realpath(content) != content:
                        print("Symbolic link : " + content)
                        continue
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
            print('Permission denied : ' + self.path)
        except FileNotFoundError:
            print('File not found : ' + self.path)
        except NotADirectoryError:
            print('Not a directory : ' + self.path)
        except OSError:
            print('Smething wrong  : ' + self.path)
