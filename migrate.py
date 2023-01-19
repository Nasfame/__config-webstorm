import os

import shutil

import platform

sources = ["keymaps","migrate.py","_windows"]
destinations = ["goland","webstorm","rubymine","pycharm","datagrip","dataspell"]

pwd = os.getcwd()

for dest in destinations:
  if dest in pwd:
    continue
  dest_path = f"../{dest}/"
  print(dest)
  for src in sources:
    destination = dest_path+src
    if os.path.isfile(src):
      if os.path.exists(destination):   os.remove(destination)
      shutil.copy2(src,destination)
    elif os.path.isdir(src):
      if os.path.exists(destination): shutil.rmtree(destination)
      shutil.copytree(src,destination,dirs_exist_ok=True)

print()
print("bye")
