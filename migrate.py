import os

import shutil

import sys

import platform

from datetime import datetime

import subprocess

sources = ["migrate.py", "git2", ".git/hooks/post-commit",
           "_windows", "_mac",
           "keymaps",
           "keymapFlags.xml", "abbrevs.xml", "editor-font.xml"  # "colors.scheme.xml",]
                                             "codestyles", "code.style.schemes.xml", "colors",
           "vcs.xml",
           "ide.general.xml",
           "log_highlighting.xml",
           "NewUIInfoService.xml",
           "advancedSettings.xml",
           ]
destinations = ["pycharm", "goland", "webstorm",
                "rubymine", "datagrip", "dataspell"]

pwd = os.getcwd()

print(f"PWD - {pwd}")

sys_args = sys.argv
if len(sys_args) > 1:
    pwd = sys_args[1]
    os.chdir(pwd)

current_config_folder = pwd.split('/')[-1]

if current_config_folder not in destinations:
    raise FileNotFoundError("is not a valid jetbrains settings repository")

if not os.path.exists(pwd):
    raise FileNotFoundError(f"config folder not found {pwd}")

print(f"CWD - {pwd}")
print("current_config_folder", current_config_folder)

dest_path_template = list(os.path.split(pwd))  # pwd.split('/')

for config_folder in destinations:
    if config_folder == current_config_folder:
        continue
    dest_path_template[-1] = config_folder
    # f"~/Nasfame/jetbrains/{dest}"
    dest_config = os.path.join(*dest_path_template)
    print("Destination", dest_config)
    for src in sources:
        print("copying", src)
        src_path = os.path.split(src)[:1]
        destination = os.path.join(dest_config, *src_path)
        if os.path.isfile(src):
            # if os.path.exists(destination):
            #   os.remove(destination)
            # Copy the file with overwrite
            # shutil.copyfile(src, destination)
            print(f"destination for {src} is {destination} ")
            if not os.path.exists(destination):
                print(f"creating dir - {destination}")
                os.makedirs(destination, exist_ok=True)
            shutil.copy2(src, destination)
        elif os.path.isdir(src):
            # if os.path.exists(destination): shutil.rmtree(destination)
            shutil.copytree(src, destination, dirs_exist_ok=True)

    with open(f"{dest_config}/sync.log", 'a') as f1:
        now_utc = datetime.utcnow()
        f1.write(f"{now_utc} {current_config_folder} | Timezone - IST")
        print("appending sync.log")

    git_cmds = [
        # ["git", "add", "."],
        "chmod -x .git/hooks/post-commit",
        "git add .",
        f"""git commit -m "synced with {current_config_folder}" """,
        "chmod +x .git/hooks/post-commit"
    ]
    # https://linuxhint.com/execute_shell_python_subprocess_run_method/
    for git_cmd in git_cmds:
        cmd = git_cmd #" ".join(git_cmd)
        print(cmd)
        result = subprocess.run(cmd, cwd=dest_config, shell=True,capture_output=True, text=True,check=True, #results in try catch
                                )
        return_code = result.returncode
        if return_code == 1:
            print(f"stderr: {result.stderr.strip()}")
            print(f"stdout: {result.stdout.strip()}")
            print(f"breaking with {return_code}")
            break

        # print(f"Return code: {result.returncode}")
        # print(f"stdout: {result.stdout.strip()}")

            # stdout=subprocess.PIPE)

    # os.system("git add .")
    # os.system(f"""git commit -m "synced with {current_config_folder}" """) #FIXME results in race condition as git hook would be triggered in the destination directory

print()
print("bye")
