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
            print(f"[{GREEN}Успешно{RESET}]")
        else:
            print(f"[{RED}Неудачно{RESET}]")
            input("Переподключите устройство и нажмите Enter")


picker = PackPicker(PACK_DIR)
client = Client(MAX_TIMEOUT)

print("Замена голосовых пакетов")
print("Автор: ryze312")
print("ПРОВЕРЕНО только на Viomi STYT02JYM.")
print("Смотрите в README_RUS.\n")

pack = picker.choose_pack("Выберите пакет: ")

try_func("Ожидание устройства", client.wait_and_get_device)
try_func("Копирование ADB оболочки на устройство", client.push, "adb_shell", "/sbin/adb_shell")
try_func("Отключение службы robotManager", client.remove, "/etc/rc.d/S90robotManager")

input("Переподключите устройство и нажмите Enter")
try_func("Ожидание устройства", client.wait_and_get_device)
try_func("Бэкап оригинальных звуков", client.pull_dir, "/usr/share/audio/mandarin/", BACKUP_DIR)
try_func("Удаление оригинальных звуков", client.shell, "rm /usr/share/audio/mandarin/*")

for file in os.listdir(pack):
    if file.endswith(".mp3"):
        try_func(f"Копирование {file}", client.push, f"{pack}/{file}", "/usr/share/audio/mandarin/")
try_func("Включение службы robotManager", client.ln, "/etc/init.d/robotManager", "/etc/rc.d/S90robotManager")

print("Готово!")
input("Нажмите Enter, чтобы выйти...")
