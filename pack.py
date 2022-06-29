import os


class PackPicker:
    def __init__(self, pack_folder: str):
        if not os.path.isdir(pack_folder):
            os.mkdir(pack_folder)

        packs = os.listdir(pack_folder)
        self.base_folder = pack_folder
        self.packs = [pack for pack in packs if os.path.isdir(f"{self.base_folder}/{pack}")]

    def print_packs(self):
        for i, pack in enumerate(self.packs):
            print(f"{i + 1}. {pack}")

    def choose_pack(self, prompt=""):
        entry = 0
        self.print_packs()
        while entry < 1 or entry > len(self.packs):
            try:
                entry = int(input(prompt))
            except ValueError:
                pass
        return self.base_folder + "/" + self.packs[entry - 1]
