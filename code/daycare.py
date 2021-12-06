from creature import *
from common import *
from species import *
from save import *
from random import getrandbits, randint, choice, choices
from json import load

class daycare:
	def __init__(self, name, randomNameFilePath:str, helpFilePath:str):
		self.name = name

		self.upgrades = dict()
