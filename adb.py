import os
from time import time

from adbutils import AdbClient, AdbDevice, AdbTimeout


class Client:
    def __init__(self, max_timeout: int):
        self.client: AdbClient = AdbClient()
        self.device: AdbDevice = None
        self.max_timeout = max_timeout

    def try_until_success(self, func, *args):
        end_time = time() + self.max_timeout
        while time() < end_time:
            try:
                return func(*args)
            except (OSError, AssertionError) as e:
                pass

        return False

    def wait_and_get_device(self):
        try:
            self.client.wait_for(timeout=self.max_timeout)
        except AdbTimeout:
            return False

        self.device = self.client.device_list()[0]
        return True

    def push(self, local_path: str, remote_path: str):
        return self.try_until_success(self.device.push, local_path, remote_path)

    def pull_file(self, remote_path: str, local_path: str):
        return self.try_until_success(self.device.sync.pull, remote_path, local_path)

    def pull_dir(self, remote_path: str, local_path: str):
        if not os.path.isdir(local_path):
            os.mkdir(local_path)

        files = self.device.sync.list(remote_path)[2:]  # Skipping . and ..

        for file in files:
            self.pull_file(remote_path + f"/{file.path}", local_path + f"/{file.path}")

    def remove(self, remote_path: str):
        return self.try_until_success(self.device.remove, remote_path)

    def shell(self, cmd: str):
        return self.try_until_success(self.device.shell, cmd)

    def ln(self, src_path, dst_path):
        return self.shell(f"ln -s {src_path} {dst_path}")
