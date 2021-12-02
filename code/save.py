from json import load, dump

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
        savefile["pigeon data"][pigeonUID] = converPigeonSave(game.allPigeons[pigeonUID])

    dump(savefile, open("testsave.json", "w"), indent=2)

def converPigeonSave(pigeon):
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

def load(gameName):
    pass
