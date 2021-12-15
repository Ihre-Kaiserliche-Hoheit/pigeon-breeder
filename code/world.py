from json import load

class World:
    def __init__(self, savename:str, worldname:str):
        self.savename = savename
        self.worldname = worldname

        self.year = 0
        self.month = 1

        self.wealth = 50


    def updateTime(self):
        self.month += 1

        if 12 < self.month:
            self.month = 1
            self.year += 1

    def command(self, command):
        command = command.lower().split()

        match command[0]:
            case "quit" | "q":
                raise EOFError

            case _:
                print("Command not found")