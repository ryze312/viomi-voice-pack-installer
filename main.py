import os.path

import colorama

from adb import Client
from pack import PackPicker

BACKUP_DIR = "Backup"
PACK_DIR = "Packs"
MAX_TIMEOUT = 17

RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
RESET = colorama.Fore.RESET


def try_func(entry, func, *args):
    result = False
    while result is False:
        print(entry, end=" ", flush=True)
        result = func(*args)
        if result is not False:
            print(f"[{GREEN}Success{RESET}]")
        else:
            print(f"[{RED}Fail{RESET}]")
            input("Reconnect device and hit enter")


picker = PackPicker(PACK_DIR)
client = Client(MAX_TIMEOUT)

print("Voice pack installer by ryze312")
print("TESTED only on Viomi STYT02JYM.")
print("Check README for more info.\n")

pack = picker.choose_pack("Choose pack: ")

try_func("Waiting for device", client.wait_and_get_device)
try_func("Pushing ADB Shell to device", client.push, "adb_shell", "/sbin/adb_shell")
try_func("Unlink robotManager from RC", client.remove, "/etc/rc.d/S90robotManager")

input("Reconnect device and hit enter")
try_func("Waiting for device", client.wait_and_get_device)
try_func("Backing up original sounds", client.pull_dir, "/usr/share/audio/mandarin/", BACKUP_DIR)
try_func("Deleting original sounds", client.shell, "rm /usr/share/audio/mandarin/*")

for file in os.listdir(pack):
    if file.endswith(".mp3"):
        try_func(f"Copying {file}", client.push, f"{pack}/{file}", "/usr/share/audio/mandarin/")
try_func("Linking robotManager to RC", client.ln, "/etc/init.d/robotManager", "/etc/rc.d/S90robotManager")

print("Done!")
input("Press Enter to exit...")
