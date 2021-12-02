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

    dump(savefile, open("../saves/" + game.name.rstrip() + ".json", "w"), indent=2)

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
        "children":pigeon.children if len(pigeon.children) == 0 else [pigeon.children[childKey].uid for childKey in pigeon.children]
    }

def loadSave(gameName):
    savefile = load(open("../saves/" + gameName + ".json", "r"))

    game = dycr.daycare(savefile["care data"]["name"], "../input/pigeonNames.json", "../input/help.txt")
    game.wealth = savefile["care data"]["wealth"]
    game.month = savefile["care data"]["month"]

    for pigeonKey in savefile["care data"]["allPigeons"]:
        game.allPigeons[pigeonKey] = convertPigeonLoad(savefile["pigeon data"][pigeonKey])

    for pigeonKey in savefile["care data"]["livingPigeons"]:
        game.pigeons[pigeonKey] = game.allPigeons[pigeonKey]

    for pigeonKey in game.allPigeons:
        if game.allPigeons[pigeonKey].parents != None:
            game.allPigeons[pigeonKey].parents = [game.allPigeons[str(parentKey)] for parentKey in game.allPigeons[pigeonKey].parents]
        if len(game.allPigeons[pigeonKey].children) != 0:
            children = game.allPigeons[pigeonKey].children
            game.allPigeons[pigeonKey].children = dict()
            for childUID in children:
                game.allPigeons[pigeonKey].children[childUID] = game.allPigeons[str(childUID)]

    return game

def convertPigeonLoad(pigeonData):
    loadedPigeon = pigeonClass(pigeonData["uid"], pigeonData["name"], pigeonData["isFemale"], pigeonData["parents"], pigeonData["genes"])

    loadedPigeon.age = pigeonData["age"]
    loadedPigeon.canReproduce = pigeonData["canReproduce"]
    loadedPigeon.isAlive = pigeonData["isAlive"]
    loadedPigeon.timesBreed = pigeonData["timesBreed"]
    loadedPigeon.didAct = pigeonData["didAct"]
    loadedPigeon.genesSequenced = pigeonData["genesSequenced"]
    loadedPigeon.children = pigeonData["children"] if len(pigeonData["children"]) != 0 else dict()

    return loadedPigeon
