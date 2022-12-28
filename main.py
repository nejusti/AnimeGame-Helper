# libs
import libs.pymemoryapi as pymem
import json
import os
from time import sleep, time
import keyboard
from rich.console import Console

# Modules
from modules.memory import Memory

global b_FrendlyMobs, b_DoubleAttack, b_NoSkillCooldown, b_AlwaysElementalSight
b_DoubleAttack = False
b_NoSkillCooldown = False
b_AlwaysElementalSight = False
b_FrendlyMobs = False


class Main():
    def __init__(self) -> None:
        processes_list = pymem.list_processes_names()

        if "GenshinImpact.exe" in processes_list:
            print('[INFO] Process found.')
            self.memory = Memory()
            self.csl = Console()

            if self.memory:
                self.load_offsets()
                self.set_hotkeys()
                self.get_addreses()
                sleep(3)
                self.draw_menu()

                while True:
                    sleep(0.1)
        else:
            print("[INFO] Process not found!")

    def set_hotkeys(self):
        try:
            with open('config/keybinds.json', "r") as keys_file:
                keys = json.load(keys_file)

                self.key_DoubleAttack = keys["DoubleAttack"]
                self.key_NoSkillCooldown = keys["NoSkillCooldown"]
                self.key_AlwaysElementalSight = keys["AlwaysElementalSight"]
                self.key_FrendlyMobs = keys["FrendlyMobs"]

                keyboard.add_hotkey(self.key_DoubleAttack, self.func_DoubleAttack)
                keyboard.add_hotkey(self.key_NoSkillCooldown, self.func_NoSkillCooldown)
                keyboard.add_hotkey(self.key_AlwaysElementalSight, self.func_AlwaysElementalSight)
                keyboard.add_hotkey(self.key_FrendlyMobs, self.func_FrendlyMobs)

                keys_file.close()

        except Exception as _error:
            print("[ERROR] " + _error)

    def draw_menu(self):
        os.system('cls')
        global b_FrendlyMobs, b_DoubleAttack, b_NoSkillCooldown, b_AlwaysElementalSight

        self.csl.print("[GISuck 3.3.0][Creator: JUSTi#6006]")

        self.csl.print("\n[Player]")
        if b_DoubleAttack:
            self.csl.print(" [green][+][/]{" + self.key_DoubleAttack + "}[green] Double Attack[/]")
        else:
            self.csl.print(" [red][-][/]{" + self.key_DoubleAttack + "}[green] Double Attack[/]")

        if b_NoSkillCooldown:
            self.csl.print(" [green][+][/]{" + self.key_NoSkillCooldown + "}[yellow] No Skill Cooldown[/]")
        else:
            self.csl.print(" [red][-][/]{" + self.key_NoSkillCooldown + "}[yellow] No Skill Cooldown[/]")

        if b_AlwaysElementalSight:
            self.csl.print(" [green][+][/]{" + self.key_AlwaysElementalSight + "}[green] Always Elemental Sight[/]")
        else:
            self.csl.print(" [red][-][/]{" + self.key_AlwaysElementalSight + "}[green] Always Elemental Sight[/]")

        self.csl.print("\n[World]")
        if b_FrendlyMobs:
            self.csl.print(" [green][+][/]{" + self.key_FrendlyMobs + "}[green] Frendly Mobs[/]")
        else:
            self.csl.print(" [red][-][/]{" + self.key_FrendlyMobs + "}[green] Frendly Mobs[/]")

    def load_offsets(self):
        try:
            with open('config/offsets.json', "r") as offsets_file:
                offsets = json.load(offsets_file)

                # Patterns
                # Player
                self.pattern_DoubleAttack = offsets['Patterns']['DoubleAttack']
                self.pattern_SkillCooldown = offsets['Patterns']['SkillCooldown']
                self.pattern_InstantBurst = offsets['Patterns']['InstantBurst']
                self.pattern_AlwaysElementalSight = offsets['Patterns']['AlwaysElementalSight']
                # World
                self.pattern_FrendlyMobs = offsets['Patterns']['FrendlyMobs']

                offsets_file.close()

        except Exception as _error:
            print("[ERROR] " + _error)

    def get_addreses(self):
        # Player
        self.addres_DoubleAttack = self.memory.get_sig('UnityPlayer.dll', self.pattern_DoubleAttack, True)
        self.addres_SkillCooldown = self.memory.get_sig('UserAssembly.dll', self.pattern_SkillCooldown, True)
        self.addres_InstantBurst = self.memory.get_sig('UserAssembly.dll', self.pattern_InstantBurst, True)
        self.addres_AlwaysElementalSight = self.memory.get_sig('UserAssembly.dll', self.pattern_AlwaysElementalSight, True)
        # World
        self.addres_FrendlyMobs = self.memory.get_sig('UserAssembly.dll', self.pattern_FrendlyMobs, True)

        # Print adresses
        print('[INFO] Found addresses')
        print(' DoubleAttack - ' + hex(self.addres_DoubleAttack))
        print(' SkillCooldown - ' + hex(self.addres_SkillCooldown))
        print(' InstantBurst - ' + hex(self.addres_InstantBurst))
        print(' AlwaysElementalSight - ' + hex(self.addres_AlwaysElementalSight))
        print(' FrendlyMobs - ' + hex(self.addres_FrendlyMobs))

    def func_DoubleAttack(self):
        global b_DoubleAttack
        b_DoubleAttack = not b_DoubleAttack
        self.memory.fucn_DoubleAttack(self.addres_DoubleAttack, b_DoubleAttack)
        self.draw_menu()

    def func_NoSkillCooldown(self):
        global b_NoSkillCooldown
        b_NoSkillCooldown = not b_NoSkillCooldown
        self.memory.fucn_NoSkillCooldown(self.addres_SkillCooldown, self.addres_InstantBurst, b_NoSkillCooldown)
        self.draw_menu()

    def func_AlwaysElementalSight(self):
        global b_AlwaysElementalSight
        b_AlwaysElementalSight = not b_AlwaysElementalSight
        self.memory.fucn_AlwaysElementalSight(self.addres_AlwaysElementalSight, b_AlwaysElementalSight)
        self.draw_menu()

    def func_FrendlyMobs(self):
        global b_FrendlyMobs
        b_FrendlyMobs = not b_FrendlyMobs
        self.memory.fucn_FrendlyMobs(self.addres_FrendlyMobs, b_FrendlyMobs)
        self.draw_menu()


if __name__ == "__main__":
    Main()
