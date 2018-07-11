# -*- coding: utf-8 -*-

import os


class FolderInfo():
  """
  FolderInfo stores a directory name and the size of
  its contents and subdirectories' FolderInfo.
  """

  def __init__(self, folder_path):
    self.absolute_path = os.path.abspath(folder_path)  # フォルダの絶対パス
    self.size_total = 0  # folder + file
    self.size_files = 0
    self.sub_dirs = []  # subdirectories' FolderInfo
    try:
      for content in os.listdir(self.absolute_path):
        content = os.path.join(self.absolute_path, content)
        if os.path.islink(content):
          # ignore symlinks
          continue
        if os.path.isfile(content):
          # content is a file
          size = os.path.getsize(content)
          self.size_total += size
          self.size_files += size
        else:
          # content is a folder
          subfolder_info = FolderInfo(content)
          self.sub_dirs.append(subfolder_info)
          self.size_total += subfolder_info.size_total
    except PermissionError:
      self.print_error('Permission denied : ')
    except FileNotFoundError:
      self.print_error('File not found : ')
    except NotADirectoryError:
      self.print_error('Not a directory : ')
    except OSError:
      self.print_error('Smething wrong : ')
    self.sub_dirs = sorted(
        self.sub_dirs, key=lambda x: x.size_total, reverse=True)

  def print_error(self, string):
    print("[FolderInfo] " + string + self.absolute_path)

  def print(self, folder_name):
    if not folder_name.startswith(self.absolute_path):
      return
    if folder_name != self.absolute_path:
      for sub_dir in self.sub_dirs:
        if folder_name.startswith(sub_dir.absolute_path):
          sub_dir.print(folder_name)
      return
    print(("Contents of " + folder_name).center(50, "-"))
    print("100.00%% %10.2fMB All contents" % (self.size_total / 1048576))
    # self.sub_dirs are sorted by its size.
    for subfolder_info in self.sub_dirs:
      print("%6.2f%% %10.2fMB %s" %
            (subfolder_info.size_total / self.size_total * 100,
             subfolder_info.size_total / 1048576,
             os.path.basename(subfolder_info.absolute_path)))
    print("%6.2f%% %10.2fMB %s" %
          (self.size_files / self.size_total * 100, self.size_files / 1048576,
           "(files in this directory)"))
