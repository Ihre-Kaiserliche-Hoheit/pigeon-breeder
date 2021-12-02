from json import load, dump
from pigeon import *
import daycare as dycr
def save(game):
    savefile = {
        "care data":{
            "name":game.name,
            "month":game.month,
            "wealth":game.wealth,
            "livingPigeons":[pigeon for pigeon in game.pigeons],
            "allPigeons":[pigeon for pigeon in game.pigeons]
        },
        "pigeon data":{
        }
    }
    for pigeonUID in game.allPigeons:
        savefile["pigeon data"][pigeonUID] = convertPigeonSave(game.allPigeons[pigeonUID])

    dump(savefile, open("testsave.json", "w"), indent=2)

def convertPigeonSave(pigeon):
    return {
        "uid":pigeon.uid,
        "name":pigeon.name,
        "age":pigeon.age,
        "isFemale":pigeon.isFemale,
        "canReproduce":pigeon.canReproduce,
        "isAlive":pigeon.isAlive,
        "timesBreed":pigeon.timesBreed,
        "didAct":pigeon.didAct,
        "genes":pigeon.genes,
        "effectiveValues":pigeon.effectiveValues,
        "genesSequenced":pigeon.genesSequenced,
        "parents":pigeon.parents if pigeon.parents == None else [parent.uid for parent in pigeon.parents],
        "children":pigeon.children if pigeon.children == None else [child.uid for child in pigeon.children]
    }

def loadSave(gameName):
    savefile = load(open(gameName, "r"))

    game = dycr.daycare(savefile["care data"]["name"], "../input/pigeonNames.json", "../input/help.txt")
    game.wealth = savefile["care data"]["wealth"]
    game.month = savefile["care data"]["month"]

    for pigeonKey in savefile["care data"]["allPigeons"]:
        game.allPigeons[pigeonKey] = convertPigeonLoad(savefile["pigeon data"][pigeonKey])

    for pigeonKey in savefile["care data"]["livingPigeons"]:
        game.pigeons[pigeonKey] = game.allPigeons[pigeonKey]

    for pigeonKey in game.allPigeons:
        if game.allPigeons[pigeonKey].parents != None:
            game.allPigeons[pigeonKey].parents = [game.allPigeons[parentKey] for parentKey in game.allPigeons[pigeonKey].parents]
        if len(game.allPigeons[pigeonKey].children) != 0:
            game.allPigeons[pigeonKey].children = [game.allPigeons[childKey] for childKey in game.allPigeons[pigeonKey].children]

    return game

def convertPigeonLoad(pigeonData):
    loadedPigeon = pigeonClass(pigeonData["uid"], pigeonData["name"], pigeonData["isFemale"], pigeonData["parents"], pigeonData["genes"])

    loadedPigeon.age = pigeonData["age"]
    loadedPigeon.canReproduce = pigeonData["canReproduce"]
    loadedPigeon.isAlive = pigeonData["isAlive"]
    loadedPigeon.timesBreed = pigeonData["timesBreed"]
    loadedPigeon.didAct = pigeonData["didAct"]
    loadedPigeon.genesSequenced = pigeonData["genesSequenced"]
    loadedPigeon.children = pigeonData["children"]

    return loadedPigeon
