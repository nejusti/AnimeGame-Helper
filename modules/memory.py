import libs.pymemoryapi as pymem


class Memory():
    def __init__(self) -> None:
        self.process = pymem.Process("GenshinImpact.exe")
        print("[INFO] Init memory module.")

    def get_sig(self, module: str, pattern: str, first: bool):
        module = self.process.get_module_info(module)

        start_address = module.BaseAddress
        end_address = module.BaseAddress + module.SizeOfImage

        if first:
            address = self.process.pattern_scan(start_address, end_address, pattern, True)
        else:
            address = self.process.pattern_scan(start_address, end_address, pattern, False)

        return address

    def fucn_DoubleAttack(self, address: int, status: bool):
        if status:
            self.process.write_ushort(address, 18192)
        else:
            self.process.write_ushort(address, 18315)

    def fucn_NoSkillCooldown(self, address_one: int, address_two, status: bool):
        if status:
            self.process.write_ushort(address_one, 4111)
            self.process.write_ushort(address_two, 4367)
        else:
            self.process.write_ushort(address_one, 4367)
            self.process.write_ushort(address_two, 4111)

    def fucn_AlwaysElementalSight(self, address: int, status: bool):
        if status:
            self.process.write_ushort(address + 2, 336)
        else:
            self.process.write_ushort(address + 2, 80)

    def fucn_FrendlyMobs(self, address: int, status: bool):
        if status:
            self.process.write_ushort(address, 47477)
        else:
            self.process.write_ushort(address, 47476)
