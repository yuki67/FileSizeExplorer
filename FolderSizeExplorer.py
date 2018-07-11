# -*- coding: utf-8 -*-
import os
import argparse
import shelve
from FolderInfo import FolderInfo


def clearify_path(path):
  """
  return unambiguous path
  """
  path = os.path.expanduser(path)
  path = os.path.expandvars(path)
  return os.path.abspath(path)


class CLI():
  """
  Command line interface main
  """

  def __init__(self):
    self.shelve_abs_path = os.getcwd() + os.path.sep + "savedShelve"
    self.args = self.parse_args()
    self.cwd = clearify_path(self.args.working_directory)
    self.folder_info = None
    if os.path.exists(self.cwd):
      os.chdir(self.cwd)
      self.initialize_folderinfo()
      self.main_loop()
      self.epilogue()
    else:
      print(self.cwd + "does not exist.")

  def is_shelve_ready_to_load(self):
    """
    check that self.shelve_abs_path exists and that the shelve has
    self.cwd in its keys.
    """
    slv = shelve.open(self.shelve_abs_path)
    if len(list(slv.keys())) == 0:
      slv.close()
      return False
    for key in slv.keys():
      if self.cwd.startswith(key):
        slv.close()
        return True
    slv.close()
    return False

  def save_shelve(self):
    """
    save self.folder_info into self.shelve_abs_path.
    """
    slv = shelve.open(self.shelve_abs_path)
    slv[os.path.dirname(self.shelve_abs_path)] = self.folder_info
    slv.close()

  def parse_args(self):
    parser = argparse.ArgumentParser(description="Show folder size.")
    parser.add_argument(
        "-d",
        dest="working_directory",
        default="." + os.path.sep,
        required=False,
        action="store",
        help="Initial working directory. Default value = ." + os.path.sep)
    return parser.parse_args()

  def change_directory(self, directory):
    if not os.path.exists(directory):
      return
    self.cwd = directory
    os.chdir(directory)
    if directory.startswith(self.folder_info.absolute_path):
      return
    print("Collectiong imformation about %s."
          " This may take some time..." % self.cwd)
    self.folder_info = FolderInfo(self.cwd)

  def initialize_folderinfo(self):
    """
    load FolderInfo of self.cwd into self.folder_info either by loading
    saved one or by creating new one.
    """
    if self.is_shelve_ready_to_load():
      while True:
        response = input("Saved shelve (%s) found. Load this shelve? [y/n]: " %
                         self.shelve_abs_path)
        if response == "y":
          print("loading...")
          slv = shelve.open(self.shelve_abs_path)
          self.folder_info = slv[self.cwd]
          slv.close()
          return
        elif response == "n":
          break
    else:
      print("Saved shelve (%s) not found." % self.shelve_abs_path)
    print("Collectiong imformation about %s."
          " This may take some time..." % self.cwd)
    self.folder_info = FolderInfo(self.cwd)

  def epilogue(self):
    """
    save self.folder_info if the user wants to, then exit.
    """
    while True:
      response = input("Save result?[y/n] : ")
      if response == "y":
        print("saving...")
        self.save_shelve()
        print("Results saved.")
        break
      elif response == "n":
        break
    print("quitting...")

  def main_loop(self):
    self.folder_info.print(self.cwd)
    while True:
      key = input("Enter folder name. (or q to quit) : ")
      if key == "":
        continue
      elif key == "q":
        break
      else:
        key = clearify_path(key)
        self.change_directory(key)
      self.folder_info.print(self.cwd)


if __name__ == "__main__":
  CLI()
